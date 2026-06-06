from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.listar_pacientes,
        name='listar_pacientes'
    ),

    path(
        'novo/',
        views.cadastrar_paciente,
        name='cadastrar_paciente'
    ),

    path(
        '<int:paciente_id>/',
        views.detalhes_paciente,
        name='detalhes_paciente'
    ),

]