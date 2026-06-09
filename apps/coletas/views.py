import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.formularios.models import Bloco, Pergunta, OpcaoPergunta, RegraPulo
from .models import Coleta, SessaoPaciente, Resposta
from .forms import ColetaForm

@login_required
def cadastrar_coleta(request):
    if request.method == 'POST':
        form = ColetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova campanha de coleta iniciada com sucesso.')
            return redirect('painel_coletas')
    else:
        form = ColetaForm()
    return render(request, 'cadastrar_coleta.html', {'form': form, 'active_page': 'coletas'})


@login_required
def painel_coletas(request):
    coletas = Coleta.objects.all().order_by('-criado_em')
    return render(request, 'painel_coletas.html', {'coletas': coletas, 'active_page': 'coletas'})

@login_required
def detalhe_coleta(request, coleta_id):
    coleta = get_object_or_404(Coleta, id=coleta_id)
    sessoes = coleta.sessoes.all().order_by('-ultima_interacao')
    return render(request, 'detalhe_coleta.html', {'coleta': coleta, 'sessoes': sessoes, 'active_page': 'coletas'})

@login_required
def pesquisador_terminar_resposta(request, sessao_id):
    sessao = get_object_or_404(SessaoPaciente, id=sessao_id)
    sessao.preenchido_por = 'pesquisador'
    
    if not sessao.formulario_atual:
        sessao.formulario_atual = sessao.coleta.formulario_parte1 if sessao.fase_atual == 'parte1' else sessao.coleta.formulario_parte2
        sessao.save()
        
    return gerenciar_fluxo_motor(request, sessao, template_name='responder_bloco_pesquisador.html', redirecionamento='pesquisador_terminar_resposta')

def responder_formulario_token(request, token):
    sessao = get_object_or_404(SessaoPaciente, token_acesso=token)
    
    if sessao.concluida or sessao.fase_atual == 'parte2':
        return redirect('resposta_sucesso', token=token)
        
    sessao.preenchido_por = 'paciente'
    if not sessao.formulario_atual:
        sessao.formulario_atual = sessao.coleta.formulario_parte1
        sessao.save()
        
    return gerenciar_fluxo_motor(request, sessao, template_name='responder_bloco.html', redirecionamento='responder_formulario_token', use_token=True)

def gerenciar_fluxo_motor(request, sessao, template_name, redirecionamento, use_token=False):
    formulario = sessao.formulario_atual
    
    if not sessao.iniciada_em:
        sessao.iniciada_em = timezone.now()
        sessao.save()

    if not sessao.bloco_atual:
        bloco_atual = formulario.blocos.order_by('ordem').first()
        sessao.bloco_atual = bloco_atual
        sessao.save()
    else:
        bloco_atual = sessao.bloco_atual

    perguntas = bloco_atual.perguntas.all().prefetch_related('opcoes')

    if request.method == 'POST':
        erros = []
        respostas_a_salvar = []

        for pergunta in perguntas:
            campo_nome = f'pergunta_{pergunta.id}'
            
            if pergunta.tipo == 'checkbox':
                valores = request.POST.getlist(campo_nome)
                if pergunta.obrigatoria and not valores:
                    erros.append(f'A pergunta "{pergunta.titulo}" é obrigatória.')
                respostas_a_salvar.append((pergunta, valores, 'multipla'))
            elif pergunta.tipo == 'matrix':
                opcoes_m = pergunta.opcoes.all()
                valores_m = {op.id: request.POST.get(f'pergunta_{pergunta.id}_linha_{op.id}') for op in opcoes_m if request.POST.get(f'pergunta_{pergunta.id}_linha_{op.id}')}
                if pergunta.obrigatoria and len(valores_m) < opcoes_m.count():
                    erros.append(f'Preencha todas as linhas da matriz: "{pergunta.titulo}".')
                respostas_a_salvar.append((pergunta, valores_m, 'matriz'))
            else:
                valor = request.POST.get(campo_nome)
                if pergunta.obrigatoria and not valor:
                    erros.append(f'A pergunta "{pergunta.titulo}" é obrigatória.')
                respostas_a_salvar.append((pergunta, valor, 'simples'))

        if erros:
            for erro in erros:
                messages.error(request, erro)
        else:
            for pergunta, dado, tipo_resp in respostas_a_salvar:
                resposta_obj, _ = Resposta.objects.get_or_create(sessao=sessao, pergunta=pergunta)
                if tipo_resp == 'multipla':
                    resposta_obj.opcoes_selecionadas.set(OpcaoPergunta.objects.filter(id__in=dado))
                    resposta_obj.valor_texto = ", ".join(dado)
                elif tipo_resp == 'matriz':
                    resposta_obj.valor_texto = json.dumps(dado)
                else:
                    resposta_obj.valor_texto = dado
                    if pergunta.tipo in ['radio', 'select']:
                        op_sel = OpcaoPergunta.objects.filter(id=dado).first()
                        if op_sel:
                            resposta_obj.opcoes_selecionadas.set([op_sel])
                resposta_obj.save()

            proximo_bloco = None
            pulo_executado = False
            for pergunta in perguntas:
                regras = RegraPulo.objects.filter(pergunta_origem=pergunta)
                for regra in regras:  # ← CORRIGIDO AQUI
                    resp_atual = Resposta.objects.filter(sessao=sessao, pergunta=pergunta).first()
                    if resp_atual and (regra.opcao_condicao in resp_atual.opcoes_selecionadas.all() or resp_atual.valor_texto == str(regra.opcao_condicao.id)):
                        proximo_bloco = regra.pergunta_destino.bloco
                        pulo_executado = True
                        break
                if pulo_executado: break

            if not pulo_executado:
                proximo_bloco = formulario.blocos.filter(ordem__gt=bloco_atual.ordem).order_by('ordem').first()

            param_redirect = {'token': sessao.token_acesso} if use_token else {'sessao_id': sessao.id}

            if proximo_bloco:
                sessao.bloco_atual = proximo_bloco
                sessao.save()
                return redirect(redirecionamento, **param_redirect)
            else:
                if sessao.fase_atual == 'parte1':
                    sessao.fase_atual = 'parte2'
                    sessao.formulario_atual = sessao.coleta.formulario_parte2
                    sessao.bloco_atual = None
                    sessao.save()
                    if use_token:
                        return redirect('resposta_sucesso', token=sessao.token_acesso)
                    else:
                        messages.success(request, 'Parte 1 concluída. Módulo transferido para Parte 2 Presencial.')
                        return redirect('detalhe_coleta', coleta_id=sessao.coleta.id)
                else:
                    sessao.fase_atual = 'finalizado'
                    sessao.concluida = True
                    sessao.bloco_atual = None
                    sessao.formulario_atual = None
                    sessao.save()
                    if use_token:
                        return redirect('resposta_sucesso', token=sessao.token_acesso)
                    else:
                        messages.success(request, 'Fluxo presencial de coleta finalizado com sucesso.')
                        return redirect('detalhe_coleta', coleta_id=sessao.coleta.id)

    return render(request, template_name, {
        'formulario': formulario, 'bloco': bloco_atual, 'perguntas': perguntas, 'sessao': sessao, 'active_page': 'coletas'
    })

def resposta_sucesso(request, token):
    sessao = get_object_or_404(SessaoPaciente, token_acesso=token)
    return render(request, 'resposta_sucesso.html', {'sessao': sessao})

@login_required
def visualizar_respostas(request, sessao_id):
    sessao = get_object_or_404(SessaoPaciente, id=sessao_id)
    # Puxa todas as respostas dadas nesta sessão
    respostas = sessao.respostas.all().select_related('pergunta').prefetch_related('opcoes_selecionadas')
    
    return render(request, 'visualizar_respostas.html', {
        'sessao': sessao,
        'respostas': respostas,
        'active_page': 'coletas'
    })

@login_required
def editar_coleta(request, coleta_id):
    coleta = get_object_or_404(Coleta, id=coleta_id)
    if request.method == 'POST':
        form = ColetaForm(request.POST, instance=coleta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campanha de coleta atualizada com sucesso.')
            return redirect('painel_coletas')
    else:
        form = ColetaForm(instance=coleta)
    return render(request, 'editar_coleta.html', {'form': form, 'coleta': coleta, 'active_page': 'coletas'})