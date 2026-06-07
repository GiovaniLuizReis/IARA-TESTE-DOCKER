from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Paciente
from .forms import PacienteForm


@login_required
def listar_pacientes(request):

    pacientes = Paciente.objects.all().order_by(
        '-id'
    )

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

            paciente = form.save()

            messages.success(
                request,
                f'Paciente {paciente.nome} cadastrado com sucesso.'
            )

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
def detalhes_paciente(
    request,
    paciente_id
):

    paciente = get_object_or_404(
        Paciente,
        id=paciente_id
    )

    return render(
        request,
        'detalhes_paciente.html',
        {
            'paciente': paciente
        }
    )


@login_required
def editar_paciente(
    request,
    paciente_id
):

    paciente = get_object_or_404(
        Paciente,
        id=paciente_id
    )

    if request.method == 'POST':

        form = PacienteForm(
            request.POST,
            instance=paciente
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Paciente atualizado com sucesso.'
            )

            return redirect(
                'detalhes_paciente',
                paciente_id=paciente.id
            )

    else:

        form = PacienteForm(
            instance=paciente
        )

    return render(
        request,
        'editar_paciente.html',
        {
            'form': form,
            'paciente': paciente
        }
    )


@login_required
def excluir_paciente(
    request,
    paciente_id
):

    paciente = get_object_or_404(
        Paciente,
        id=paciente_id
    )

    if request.method == 'POST':

        paciente.delete()

        messages.success(
            request,
            'Paciente removido com sucesso.'
        )

        return redirect(
            'listar_pacientes'
        )

    return render(
        request,
        'excluir_paciente.html',
        {
            'paciente': paciente
        }
    )