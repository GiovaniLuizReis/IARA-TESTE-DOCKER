from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel_coletas, name='painel_coletas'),
    path('<int:coleta_id>/', views.detalhe_coleta, name='detalhe_coleta'),
    path('sessao/<int:sessao_id>/aplicar/', views.pesquisador_terminar_resposta, name='pesquisador_terminar_resposta'),
    
    # Rotas públicas do Paciente (Sem Login)
    path('responder/<uuid:token>/', views.responder_formulario_token, name='responder_formulario_token'),
    path('responder/<uuid:token>/sucesso/', views.resposta_sucesso, name='resposta_sucesso'),
    path('sessao/<int:sessao_id>/respostas/', views.visualizar_respostas, name='visualizar_respostas'),
    path('novo/', views.cadastrar_coleta, name='cadastrar_coleta'),
    path('novo/', views.cadastrar_coleta, name='cadastrar_coleta'),
    path('<int:coleta_id>/editar/', views.editar_coleta, name='editar_coleta'),

]