from django.urls import path, include
from apps.usuarios import views
# Remova o auth_views se não for usar em mais nada, ou apenas ajuste a linha abaixo:
from .views import login_view, logout_view

urlpatterns = [
    path('', login_view, name='home'),

    # MUDANÇA AQUI: Em vez de usar a view nativa do Django, usamos a sua!
    path('contas/login/', login_view, name='login'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('desconectado-inatividade/', views.timeout_view, name='timeout'),

    path('contas/reset/<uidb64>/<token>/', views.CriarSenhaView.as_view(), 
         name='password_reset_confirm'),

    path('contas/', include('django.contrib.auth.urls')),

    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/excluir/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
]