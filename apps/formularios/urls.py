from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_formularios, name='listar_formularios'),
    path('novo/', views.cadastrar_formulario, name='criar_formulario'),
    path('<int:formulario_id>/', views.editar_formulario, name='editar_formulario'),
    path('<int:formulario_id>/excluir/', views.excluir_formulario, name='excluir_formulario'),
    path('<int:formulario_id>/estrutura/', views.gerenciar_estrutura, name='gerenciar_estrutura'),
    
    path('<int:formulario_id>/bloco/novo/', views.cadastrar_bloco, name='cadastrar_bloco'),
    path('bloco/<int:bloco_id>/editar/', views.editar_bloco, name='editar_bloco'),
    path('bloco/<int:bloco_id>/excluir/', views.excluir_bloco, name='excluir_bloco'),
    
    path('bloco/<int:bloco_id>/pergunta/novo/', views.cadastrar_pergunta, name='cadastrar_pergunta'),
    path('pergunta/<int:pergunta_id>/editar/', views.editar_pergunta, name='editar_pergunta'),
    path('pergunta/<int:pergunta_id>/excluir/', views.excluir_pergunta, name='excluir_pergunta'),
    path('pergunta/<int:pergunta_id>/visualizar/', views.visualizar_pergunta, name='visualizar_pergunta'),
    
    path('pergunta/<int:pergunta_id>/opcao/novo/', views.cadastrar_opcao, name='cadastrar_opcao'),
    path('opcao/<int:opcao_id>/editar/', views.editar_opcao, name='editar_opcao'),
    path('opcao/<int:opcao_id>/excluir/', views.excluir_opcao, name='excluir_opcao'),
    
    path('pergunta/<int:pergunta_id>/regra/novo/', views.configurar_regra_pulo, name='configurar_regra_pulo'),
    path('regra/<int:regra_id>/excluir/', views.excluir_regra_pulo, name='excluir_regra_pulo'),
]