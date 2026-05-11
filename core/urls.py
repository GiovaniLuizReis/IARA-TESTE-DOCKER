"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from asyncio.log import logger

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

'''Teste'''
import logging
from django.http import JsonResponse


def test_logging_view(request):
    try:
        data = {'user': 'leticia', 'email': 'leticia@contato.com'}
        # Força um erro proposital para testar o log
        raise ValueError("Erro simulado no envio de email")
    except Exception as e:
        # Loga o erro usando o logger configurado
        logger.error(f"{str(e)} | {str(data)}")
        return JsonResponse({"status": "error", "message": "Ocorreu um erro."})
    

'''Fim teste'''
from django.urls import path 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test-logging/', test_logging_view, name='test_logging'), #teste
]

if settings.DEBUG: # update 03/11/2024: (em homologa com debug true adiciona rota static)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)