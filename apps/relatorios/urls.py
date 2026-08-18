from django.urls import path
from . import views

app_name = 'relatorios' # Namespace para evitar conflitos de nomes

urlpatterns = [
    path('', views.painel_relatorios, name='painel'),
    path('csv/', views.exportar_csv, name='exportar_csv'),
    path('pdf/', views.exportar_pdf, name='exportar_pdf'),
]