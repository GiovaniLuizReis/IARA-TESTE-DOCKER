from django.urls import path
from .views import login_view, dashboard_view
from apps.usuarios import views

urlpatterns = [
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('desconectado-inatividade/',  views.timeout_view, name='timeout'), 
]