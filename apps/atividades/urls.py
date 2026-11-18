from django.urls import path
from . import views

urlpatterns = [
    # =========================================================================
    # GESTÃO DA PESQUISA (Acesso Restrito aos Pesquisadores)
    # =========================================================================
    # Painel geral que lista todos os participantes do sistema
    path('', views.painel_atividades, name='painel_atividades'),
    
    # Detalhes de um participante específico e gerenciamento de seus cards
    path('participante/<int:participante_id>/', views.detalhe_participante_atividades, name='detalhe_participante_atividades'),
    
    # Ação para gerar os formulários da Parte 2 (Laboratório) para o participante
    path('participante/<int:participante_id>/gerar-p2/', views.gerar_atividades_p2, name='gerar_atividades_p2'),
    
    # Rota para o pesquisador assumir e preencher um formulário junto com o participante
    path('assumir/<int:atividade_id>/', views.pesquisador_assumir_atividade, name='pesquisador_assumir_atividade'),
    
    # Histórico de leitura para visualizar as respostas de um formulário já concluído
    path('atividade/<int:atividade_id>/respostas/', views.visualizar_respostas, name='visualizar_respostas'),

    # NOVO: Histórico de auditoria e linha do tempo da atividade
    path('atividade/<int:atividade_id>/historico/', views.visualizar_historico_atividade, name='visualizar_historico_atividade'),


    # =========================================================================
    # FLUXO DO PARTICIPANTE (Acesso via Token Seguro por E-mail)
    # =========================================================================
    # Hub central contendo os cards de progresso dos questionários (Parte 1)
    path('responder/<uuid:token>/', views.painel_participante_token, name='painel_participante_token'),
    
    # Questionário dinâmico passo a passo aberto ao clicar em um card específico
    path('questionario/<uuid:token>/', views.responder_atividade_token, name='responder_atividade_token'),


    # =========================================================================
    # ENDPOINTS DE SISTEMA e APIS
    # =========================================================================
    # Tela genérica de sucesso após finalizações de fluxos externos
    path('sucesso/', views.resposta_sucesso, name='resposta_sucesso'),
    
    # API assíncrona utilizada pelo mecanismo de Auto-save das perguntas
    path('api/salvar-resposta/<int:atividade_id>/', views.salvar_resposta_assincrona, name='salvar_resposta_assincrona'),

    # NOVO: API assíncrona para registrar pausa/interrupção do formulário
    path('api/salvar-pausa/<int:atividade_id>/', views.registrar_pausa_assincrona, name='registrar_pausa_assincrona'),
]