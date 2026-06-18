from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.listar_participantes,
        name='listar_participantes'
    ),

    path(
        'novo/',
        views.cadastrar_participante,
        name='cadastrar_participante'
    ),

    path(
        '<int:participante_id>/',
        views.detalhes_participante,
        name='detalhes_participante'
    ),
    path(
        '<int:participante_id>/reenviar-link/',
        views.reenviar_link_participante,
        name='reenviar_link_participante'
    ),
    path('<int:participante_id>/excluir/', views.excluir_participante, name='excluir_participante'),

]