import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages

from .models import Atividade, Resposta, HistoricoAtividade
from apps.participantes.models import Participante
from apps.formularios.models import Formulario, Pergunta, OpcaoPergunta


@login_required
def painel_atividades(request):
    """Lista todos os participantes para monitorização da equipa de pesquisa."""
    participantes = Participante.objects.all().order_by('-id')
    return render(request, 'painel_atividades.html', {
        'participantes': participantes, 
        'active_page': 'atividades'
    })


@login_required
def detalhe_participante_atividades(request, participante_id):
    """Exibe o painel de gerenciamento de cards de um participante específico."""
    participante = get_object_or_404(Participante, id=participante_id)
    atividades = participante.atividades.all().select_related('formulario')
    return render(request, 'detalhe_participante.html', {
        'participante': participante, 
        'atividades': atividades, 
        'active_page': 'atividades'
    })


@login_required
def pesquisador_assumir_atividade(request, atividade_id):
    """Permite ao pesquisador assumir e preencher o formulário junto com o participante."""
    atividade = get_object_or_404(Atividade, id=atividade_id)
    
    # Rastreio no Histórico
    HistoricoAtividade.objects.create(
        atividade=atividade,
        tipo_acao='assumir',
        acao=f"Pesquisador {request.user.get_full_name() or request.user.username} assumiu o preenchimento.",
        usuario_responsavel=request.user
    )
    return motor_resposta(request, atividade, use_token=False)


@login_required
def visualizar_respostas(request, atividade_id):
    """Exibe um relatório de leitura estático com as respostas guardadas de um formulário concluído."""
    atividade = get_object_or_404(Atividade, id=atividade_id)
    formulario = atividade.formulario
    
    # Carrega perguntas e opções otimizando o acesso ao banco
    perguntas = formulario.perguntas.all().prefetch_related('opcoes')
    
    # Mapeia as respostas dadas nesta atividade
    respostas_dadas = {
        resp.pergunta_id: resp 
        for resp in atividade.respostas.all().prefetch_related('opcoes_selecionadas')
    }
    
    # Vincula a resposta diretamente ao objeto da pergunta para simplificar o loop no HTML
    for pergunta in perguntas:
        pergunta.resposta_registada = respostas_dadas.get(pergunta.id)
    
    return render(request, 'visualizar_respostas.html', {
        'atividade': atividade,
        'formulario': formulario,
        'perguntas': perguntas
    })


@login_required
def visualizar_historico_atividade(request, atividade_id):
    """Exibe o histórico cronológico detalhado de uma atividade."""
    atividade = get_object_or_404(Atividade, id=atividade_id)
    historico = atividade.historico.all()
    
    return render(request, 'visualizar_historico.html', {
        'atividade': atividade,
        'historico': historico,
    })


@login_required
def gerar_atividades_p2(request, participante_id):
    """Atribui ao participante qualquer formulário ativo que ele ainda não tenha recebido."""
    if request.method == 'POST':
        participante = get_object_or_404(Participante, id=participante_id)
        
        # Procura por todos os formulários ativos no sistema (P1, P2, exames, etc.)
        formularios_ativos = Formulario.objects.filter(ativo=True)
        
        if not formularios_ativos.exists():
            messages.warning(request, 'Nenhum formulário ou instrumento de recolha está ativo no sistema.')
            return redirect('detalhe_participante_atividades', participante_id=participante.id)
            
        criados = 0
        for formulario in formularios_ativos:
            # get_or_create impede a duplicação se o instrumento já foi associado ao participante
            obj, created = Atividade.objects.get_or_create(
                participante=participante,
                formulario=formulario,
                defaults={'status': 'nao_iniciado'}
            )
            if created:
                criados += 1
                
        if criados > 0:
            messages.success(request, f'{criados} nova(s) atividade(s) atribuída(s) com sucesso!')
        else:
            messages.info(request, 'O participante já possui todos os formulários ativos atribuídos.')
            
    return redirect('detalhe_participante_atividades', participante_id=participante.id)


def painel_participante_token(request, token):
    """Hub central de cards de acesso seguro para o participante preencher online (Parte 1)."""
    atividade_ref = get_object_or_404(Atividade, token_acesso=token)
    participante = atividade_ref.participante
    
    atividades = Atividade.objects.filter(
        participante=participante,
        formulario__parte='P1'
    ).select_related('formulario').order_by('formulario__ordem', 'id')
    
    return render(request, 'painel_participante.html', {
        'participante': participante,
        'atividades': atividades
    })


def responder_atividade_token(request, token):
    """Direciona o participante ao questionário passo a passo se não estiver concluído."""
    atividade = get_object_or_404(Atividade, token_acesso=token)
    
    if atividade.status == 'concluido':
        return redirect('painel_participante_token', token=atividade.token_acesso)
        
    return motor_resposta(request, atividade, use_token=True)


def motor_resposta(request, atividade, use_token=False):
    """Mecanismo interno comum para renderização de formulários (Pesquisador ou Participante)."""
    formulario = atividade.formulario
    perguntas = formulario.perguntas.all().prefetch_related('opcoes')
    
    if atividade.status == 'nao_iniciado':
        atividade.status = 'em_andamento'
        atividade.data_inicio = timezone.now()
        atividade.save()
        
        # Rastreio de Início no Histórico
        HistoricoAtividade.objects.create(
            atividade=atividade,
            tipo_acao='inicio',
            acao="Preenchimento Iniciado",
            usuario_responsavel=request.user if not use_token else None
        )
    elif atividade.status == 'em_andamento':
        # Rastreio de Retomada no Histórico
        HistoricoAtividade.objects.create(
            atividade=atividade,
            tipo_acao='retomada',
            acao="Preenchimento Retomado",
            usuario_responsavel=request.user if not use_token else None
        )

    respostas_dadas = {resp.pergunta_id: resp for resp in atividade.respostas.all()}

    return render(request, 'responder_atividade.html', {
        'atividade': atividade, 
        'formulario': formulario, 
        'perguntas': perguntas, 
        'respostas_dadas': respostas_dadas,
        'use_token': use_token,
        'ultima_pergunta_id': atividade.ultima_pergunta_acessada.id if atividade.ultima_pergunta_acessada else None
    })


def resposta_sucesso(request):
    """Página de conclusão de fluxos externos."""
    return render(request, 'resposta_sucesso.html')


@csrf_exempt
def salvar_resposta_assincrona(request, atividade_id):
    """Endpoint AJAX para gravação de respostas em tempo real pergunta por pergunta, gerando histórico de alterações."""
    if request.method == 'POST':
        atividade = get_object_or_404(Atividade, id=atividade_id)
        dados = json.loads(request.body)
        
        pergunta_id = dados.get('pergunta_id')
        valor = dados.get('valor')
        tipo = dados.get('tipo')
        
        pergunta = get_object_or_404(Pergunta, id=pergunta_id)
        
        # Tenta buscar a resposta existente para auditar alterações
        resposta_obj = Resposta.objects.filter(atividade=atividade, pergunta=pergunta).first()
        valor_anterior = None
        nova_criacao = False

        if resposta_obj:
            valor_anterior = resposta_obj.valor_texto
        else:
            resposta_obj = Resposta(atividade=atividade, pergunta=pergunta)
            nova_criacao = True

        # Processamento do tipo de dado
        if tipo == 'checkbox':
            if nova_criacao:
                 resposta_obj.save()
            opcoes = OpcaoPergunta.objects.filter(id__in=valor)
            resposta_obj.opcoes_selecionadas.set(opcoes)
            resposta_obj.valor_texto = ", ".join([op.texto for op in opcoes])
        elif tipo in ['radio', 'select']:
            if nova_criacao:
                 resposta_obj.save()
            op_sel = OpcaoPergunta.objects.filter(id=valor).first()
            if op_sel:
                resposta_obj.opcoes_selecionadas.set([op_sel])
                resposta_obj.valor_texto = op_sel.texto
        else:
            resposta_obj.valor_texto = str(valor)
            if nova_criacao:
                resposta_obj.save()
            
        resposta_obj.save()

        # Determina o usuário responsável (se logado ou via link do participante)
        usuario = request.user if request.user.is_authenticated else None

        # Registra a alteração no Histórico se a resposta já existia e o valor mudou
        if not nova_criacao and valor_anterior != resposta_obj.valor_texto:
            detalhes = {
                'pergunta': pergunta.titulo,
                'valor_anterior': valor_anterior,
                'valor_novo': resposta_obj.valor_texto
            }
            HistoricoAtividade.objects.create(
                atividade=atividade,
                tipo_acao='alteracao',
                acao=f"Resposta alterada: {pergunta.titulo}",
                usuario_responsavel=usuario,
                detalhes_json=detalhes
            )

        # Atualiza o checkpoint indicando onde o usuário parou
        atividade.ultima_pergunta_acessada = pergunta

        # Recalcular métricas de progresso
        total_perguntas = atividade.formulario.perguntas.count()
        respostas_contadas = atividade.respostas.count()
        if total_perguntas > 0:
            progresso = int((respostas_contadas / total_perguntas) * 100)
            atividade.progresso_percentual = progresso
            if progresso >= 100:
                atividade.status = 'concluido'
                atividade.data_fim = timezone.now()
                
                if atividade.data_inicio:
                    delta = atividade.data_fim - atividade.data_inicio
                    atividade.tempo_gasto_segundos = int(delta.total_seconds())
                
                # Rastreio de Conclusão no Histórico
                HistoricoAtividade.objects.create(
                    atividade=atividade,
                    tipo_acao='conclusao',
                    acao="Formulário Concluído",
                    usuario_responsavel=usuario
                )

        atividade.save()
        return JsonResponse({'status': 'success', 'progresso': atividade.progresso_percentual})
    
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def registrar_pausa_assincrona(request, atividade_id):
    """Endpoint AJAX para registrar quando o formulário é pausado (fechamento de janela ou saída)."""
    if request.method == 'POST':
        atividade = get_object_or_404(Atividade, id=atividade_id)
        usuario = request.user if request.user.is_authenticated else None
        
        # Evita registrar múltiplas pausas consecutivas (spam no histórico)
        ultimo_registro = atividade.historico.last()
        if ultimo_registro and ultimo_registro.tipo_acao != 'pausa':
            HistoricoAtividade.objects.create(
                atividade=atividade,
                tipo_acao='pausa',
                acao="Preenchimento Pausado/Interrompido",
                usuario_responsavel=usuario
            )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)