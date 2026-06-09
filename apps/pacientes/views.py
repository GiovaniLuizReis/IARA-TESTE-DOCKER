from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .models import Paciente
from .forms import PacienteForm
from apps.coletas.models import Coleta, SessaoPaciente


@login_required
def listar_pacientes(request):
    pacientes = Paciente.objects.all().order_by('-id')
    return render(
        request,
        'listar_pacientes.html',
        {
            'pacientes': pacientes
        }
    )


@login_required
def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)

        if form.is_valid():
            # 1. Salva o paciente no banco (gera automaticamente a identificação baseada no Estado/Centro)
            paciente = form.save()

            # 2. Busca a campanha de Coleta que está ativa ("Em Andamento") no momento
            coleta_ativa = Coleta.objects.filter(status='em_andamento').first()

            if coleta_ativa:
                # 3. Cria a sessão do paciente vinculada à Parte 1 do formulário
                sessao = SessaoPaciente.objects.create(
                    coleta=coleta_ativa,
                    email_paciente=paciente.email,
                    fase_atual='parte1',
                    formulario_atual=coleta_ativa.formulario_parte1
                )

                # 4. Constrói o URL absoluto com o token UUID único
                link_formulario = request.build_absolute_uri(
                    reverse('responder_formulario_token', args=[sessao.token_acesso])
                )
                
                assunto = 'IARA-Saúde: Acesso ao Questionário de Pesquisa'
                mensagem = f"""Olá, {paciente.nome}.

Seu cadastro na pesquisa IARA-SAÚDE foi realizado com sucesso.
Seu código de identificação é: {paciente.identificacao}

Para acessar o seu questionário, clique no link abaixo:
{link_formulario}

Este link é seguro, intransferível e salva seu progresso automaticamente.
"""
                try:
                    send_mail(
                        subject=assunto,
                        message=mensagem,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[paciente.email],
                        fail_silently=False,
                    )
                    messages.success(request, f'Paciente {paciente.nome} cadastrado! E-mail com link enviado com sucesso.')
                except Exception as e:
                    messages.warning(request, f'Paciente salvo, mas ocorreu um erro ao enviar o e-mail: {e}')
            else:
                messages.warning(request, f'Paciente {paciente.nome} cadastrado com sucesso, mas NENHUMA COLETA ESTÁ EM ANDAMENTO para gerar o link.')

            return redirect('listar_pacientes')
    else:
        form = PacienteForm()

    return render(
        request,
        'cadastrar_paciente.html',
        {
            'form': form,
            'active_page': 'pacientes'
        }
    )


@login_required
def detalhes_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    return render(
        request,
        'detalhes_paciente.html',
        {
            'paciente': paciente
        }
    )


@login_required
def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)

        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente atualizado com sucesso.')
            return redirect('detalhes_paciente', paciente_id=paciente.id)
    else:
        form = PacienteForm(instance=paciente)

    return render(
        request,
        'editar_paciente.html',
        {
            'form': form,
            'paciente': paciente
        }
    )


@login_required
def excluir_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Paciente removido com sucesso.')
        return redirect('listar_pacientes')

    return render(
        request,
        'excluir_paciente.html',
        {
            'paciente': paciente
        }
    )

@login_required
def reenviar_link_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    coleta_ativa = Coleta.objects.filter(status='em_andamento').first()

    if not coleta_ativa:
        messages.error(request, 'Nenhuma coleta em andamento para gerar o link.')
        return redirect('listar_pacientes')

    # Busca se o paciente já tem sessão nesta coleta; se não tiver, cria uma nova.
    sessao, created = SessaoPaciente.objects.get_or_create(
        coleta=coleta_ativa,
        email_paciente=paciente.email,
        defaults={
            'fase_atual': 'parte1',
            'formulario_atual': coleta_ativa.formulario_parte1
        }
    )

    # Gera o link
    link_formulario = request.build_absolute_uri(
        reverse('responder_formulario_token', args=[sessao.token_acesso])
    )
    
    assunto = 'IARA-Saúde: Acesso ao Questionário (Reenvio)'
    mensagem = f"""Olá, {paciente.nome}.

Aqui está o seu link de acesso para a pesquisa IARA-SAÚDE:
{link_formulario}

Este link é seguro, intransferível e salva seu progresso automaticamente.
"""
    try:
        send_mail(
            subject=assunto,
            message=mensagem,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[paciente.email],
            fail_silently=False,
        )
        messages.success(request, f'Link reenviado com sucesso para {paciente.email}!')
    except Exception as e:
        messages.error(request, f'Erro ao reenviar o e-mail: {e}')

    return redirect('listar_pacientes')