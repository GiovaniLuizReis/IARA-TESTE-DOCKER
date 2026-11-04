from django.urls import path, include
from apps.usuarios import views
from .views import login_view, logout_view

urlpatterns = [
   
    # path("accounts/", include("django.contrib.auth.urls")),
    # path('contas/', include('django.contrib.auth.urls')),

    # Recurperar e criar senha
    path('resetar-senha/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('contas/reset/<uidb64>/<token>/', views.CriarSenhaView.as_view(), name='password_reset_confirm'),

    #Reenviar link de acesso
    path('usuarios/<int:usuario_id>/reenviar-link/', views.reenviar_link_acesso, name='reenviar_link_acesso'),
    
    # Login e Logout
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('contas/login/', login_view, name='login_contas'),
    path('logout/', logout_view, name='logout'),
    
    # Usuarios em geral 
    path('desconectado-inatividade/', views.timeout_view, name='timeout'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/excluir/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
]