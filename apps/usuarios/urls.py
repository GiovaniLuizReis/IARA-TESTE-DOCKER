from django.urls import path
from .views import login_view, logout_view
from apps.usuarios import views
#from dashboard.views import dashboard_view

urlpatterns = [
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    #path('dashboard/', dashboard_view, name='dashboard'),
    path('desconectado-inatividade/',  views.timeout_view, name='timeout'),
    path('usuarios/',views.listar_usuarios,name='listar_usuarios'),
    path('usuarios/editar/<int:usuario_id>/',views.editar_usuario,name='editar_usuario'),
    path('desconectado-inatividade/',views.timeout_view,name='timeout'),

]