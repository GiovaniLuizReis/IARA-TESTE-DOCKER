from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from apps.atividades.models import Atividade
from apps.formularios.models import Formulario
from .models import Participante
from .forms import ParticipanteForm

@login_required
def cadastrar_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)

        if form.is_valid():
            # 1. Guarda o participante no banco de dados
            participante = form.save()

            # 2. Procura todos os formulários estruturais que estão ativos no sistema
            formularios_ativos = Formulario.objects.filter(ativo=True).order_by('ordem')

            if formularios_ativos.exists():
                atividades_criadas = []
                
                # 3. Cria uma instância de Atividade para cada formulário temático ativo
                for formulario in formularios_ativos:
                    atv = Atividade.objects.create(
                        participante=participante,
                        formulario=formulario,
                        status='nao_iniciado'
                    )
                    atividades_criadas.append(atv)

                # 4. Seleciona a primeira atividade da Parte 1 (P1) para servir como referência de entrada
                atividade_chave = next(
                    (a for a in atividades_criadas if a.formulario.parte == 'P1'), 
                    atividades_criadas[0]
                )
                
                # 5. Constrói o URL absoluto apontando diretamente para o painel geral de cards
                link_painel = request.build_absolute_uri(
                    reverse('painel_participante_token', args=[atividade_chave.token_acesso])
                )
                
                assunto = 'IARA-Saúde: Acesso ao Painel de Pesquisa'
                mensagem = f"""Olá, {participante.nome}.

Seu cadastro na pesquisa IARA-SAÚDE foi realizado com sucesso.
Seu código de identificação é: {participante.identificacao}

Para acessar o seu painel de questionários, clique no link abaixo:
{link_painel}

Este link é seguro, intransferível e guarda o seu progresso automaticamente a cada resposta.
"""
                try:
                    send_mail(
                        subject=assunto,
                        message=mensagem,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[participante.email],
                        fail_silently=False,
                    )
                    messages.success(request, f'Participante {participante.nome} cadastrado e atividades geradas com sucesso!')
                except Exception as e:
                    messages.warning(request, f'Participante guardado, mas ocorreu um erro ao enviar o e-mail: {e}')
            else:
                messages.warning(request, f'Participante {participante.nome} cadastrado, mas nenhum formulário ativo foi encontrado para gerar as atividades.')

            return redirect('listar_participantes')
    else:
        form = ParticipanteForm()

    return render(
        request,
        'cadastrar_participante.html',
        {
            'form': form,
            'active_page': 'participantes'
        }
    )


@login_required
def listar_participantes(request):
    participantes = Participante.objects.all().order_by('-id')
    return render(
        request,
        'listar_participantes.html',
        {
            'participantes': participantes,
            'active_page': 'participantes'
        }
    )


@login_required
def detalhes_participante(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)
    return render(
        request,
        'detalhes_participante.html',
        {
            'participante': participante,
            'active_page': 'participantes'
        }
    )


@login_required
def editar_participante(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)

    if request.method == 'POST':
        form = ParticipanteForm(request.POST, instance=participante)

        if form.is_valid():
            form.save()
            messages.success(request, 'Participante atualizado com sucesso.')
            return redirect('detalhes_participante', participante_id=participante.id)
    else:
        form = ParticipanteForm(instance=participante)

    return render(
        request,
        'editar_participante.html',
        {
            'form': form,
            'participante': participante,
            'active_page': 'participantes'
        }
    )


@login_required
def excluir_participante(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)

    if request.method == 'POST':
        participante.delete()
        messages.success(request, 'Participante removido com sucesso.')
        return redirect('listar_participantes')

    return render(
        request,
        'excluir_participante.html',
        {
            'participante': participante,
            'active_page': 'participantes'
        }
    )


@login_required
def reenviar_link_participante(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id)
    
    # 1. Procura uma atividade ativa da Parte 1 vinculada a este participante
    atividade_chave = Atividade.objects.filter(
        participante=participante,
        formulario__parte='P1'
    ).first()

    # 2. Caso o participante não possua nenhuma atividade na Parte 1, busca qualquer atividade vinculada
    if not atividade_chave:
        atividade_chave = Atividade.objects.filter(participante=participante).first()

    if not atividade_chave:
        messages.error(request, 'Nenhuma atividade encontrada para gerar o link deste participante.')
        return redirect('listar_participantes')

    # 3. Reconstrói a URL de acesso apontando corretamente para o painel geral de cards (Hub)
    link_painel = request.build_absolute_uri(
        reverse('painel_participante_token', args=[atividade_chave.token_acesso])
    )
    
    assunto = 'IARA-Saúde: Acesso ao Painel de Pesquisa (Reenvio)'
    mensagem = f"""Olá, {participante.nome}.

Aqui está o seu link de acesso atualizado para o painel de questionários da pesquisa IARA-SAÚDE:
{link_painel}

Este link é seguro, intransferível e retoma exatamente de onde parou.
"""
    try:
        send_mail(
            subject=assunto,
            message=mensagem,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[participante.email],
            fail_silently=False,
        )
        messages.success(request, f'Link do painel reenviado com sucesso para {participante.email}!')
    except Exception as e:
        messages.error(request, f'Erro ao reenviar o e-mail: {e}')

    return redirect('listar_participantes')