from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    # path('dashboard/', dashboard_view, name='dashboard'),
    path('desconectado-inatividade/',  views.timeout_view, name='timeout'),
    path('usuarios/',views.listar_usuarios,name='listar_usuarios'),
    path('usuarios/editar/<int:usuario_id>/',views.editar_usuario,name='editar_usuario'),
    path('desconectado-inatividade/',views.timeout_view,name='timeout'),

]
