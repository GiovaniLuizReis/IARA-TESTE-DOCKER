from django.shortcuts import render, redirect

from .forms import PacienteForm


def cadastrar_paciente(request):

    if request.method == 'POST':

        form = PacienteForm(
            request.POST
        )

        if form.is_valid():

            paciente = form.save()

            return redirect(
                'listar_pacientes'
            )

    else:

        form = PacienteForm()

    return render(
        request,
        'pacientes/cadastrar.html',
        {
            'form': form
        }
    )