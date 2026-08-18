from django.urls import path, include
from apps.usuarios import views
from .views import login_view, logout_view

urlpatterns = [
    # 1º - ROTAS ORIGINAIS DO DJANGO NO TOPO
    # Ele carrega os padrões dele primeiro, para nós sobrescrevermos depois.
    path("accounts/", include("django.contrib.auth.urls")),
    path('contas/', include('django.contrib.auth.urls')),

    # 2º - RECUPERAÇÃO DE SENHA CUSTOMIZADA (Vence na busca pelo 'name')
    path('resetar-senha/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('contas/reset/<uidb64>/<token>/', views.CriarSenhaView.as_view(), name='password_reset_confirm'),
    
    # 3º - SEU LOGIN CUSTOMIZADO
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('contas/login/', login_view, name='login_contas'),
    path('logout/', logout_view, name='logout'),
    
    # 4º - RESTANTE DO SEU SISTEMA
    path('desconectado-inatividade/', views.timeout_view, name='timeout'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/excluir/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
]