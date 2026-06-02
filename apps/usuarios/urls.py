from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards por perfil
    path('dashboard/administrador/', views.dashboard_adm_view, name='dashboard_adm'),
    path('dashboard/pesquisador/', views.dashboard_pes_view, name='dashboard_pes'),
    path('dashboard/atendente/', views.dashboard_ate_view, name='dashboard_ate'),
    path('dashboard/paciente/', views.dashboard_pac_view, name='dashboard_pac'),

    # Superuser
    path('escolha-acesso/', views.escolha_acesso_view, name='escolha_acesso'),

    # Sessão
    path('desconectado-inatividade/', views.timeout_view, name='timeout'),
]
