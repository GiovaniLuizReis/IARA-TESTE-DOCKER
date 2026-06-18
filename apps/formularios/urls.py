from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_formularios, name='listar_formularios'),
    path('novo/', views.cadastrar_formulario, name='cadastrar_formulario'),
    path('<int:formulario_id>/editar/', views.editar_formulario, name='editar_formulario'),
    path('<int:formulario_id>/excluir/', views.excluir_formulario, name='excluir_formulario'),
    
    # Estrutura interna do formulário (Perguntas)
    path('<int:formulario_id>/gerenciar/', views.gerenciar_estrutura, name='gerenciar_estrutura'),
    path('<int:formulario_id>/pergunta/nova/', views.cadastrar_pergunta, name='cadastrar_pergunta'),
    path('pergunta/<int:pergunta_id>/editar/', views.editar_pergunta, name='editar_pergunta'),
    path('pergunta/<int:pergunta_id>/excluir/', views.excluir_pergunta, name='excluir_pergunta'),
    path('pergunta/<int:pergunta_id>/visualizar/', views.visualizar_pergunta, name='visualizar_pergunta'),
    path('<int:formulario_id>/preview/', views.preview_formulario, name='preview_formulario'),
    
    # Opções e Regras
    path('pergunta/<int:pergunta_id>/opcao/nova/', views.cadastrar_opcao, name='cadastrar_opcao'),
    path('opcao/<int:opcao_id>/editar/', views.editar_opcao, name='editar_opcao'),
    path('opcao/<int:opcao_id>/excluir/', views.excluir_opcao, name='excluir_opcao'),
    path('pergunta/<int:pergunta_id>/regra/nova/', views.configurar_regra_pulo, name='configurar_regra_pulo'),
    path('regra/<int:regra_id>/excluir/', views.excluir_regra_pulo, name='excluir_regra_pulo'),
]