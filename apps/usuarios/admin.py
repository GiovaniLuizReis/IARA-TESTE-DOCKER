from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario, CentroInvestigacao

# 1. Registrando os Centros de Investigação no Painel Admin
@admin.register(CentroInvestigacao)
class CentroInvestigacaoAdmin(admin.ModelAdmin):
    list_display = ('estado', 'numero', 'nome')
    list_filter = ('estado',)
    ordering = ('estado', 'numero')


# 2. Atualizando o Painel de Usuários
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    ordering = ['email']

    # Removido o 'estado' e adicionado 'cpf' para facilitar a visualização na lista
    list_display = [
        'email',
        'first_name',
        'last_name',
        'cpf',
        'identificacao',
        'tipo_usuario',
        'centro', 
        'is_staff',
    ]

    # Filtros laterais para ajudar a achar usuários rapidamente
    list_filter = ['tipo_usuario', 'centro', 'is_staff', 'is_active']

    search_fields = [
        'email',
        'first_name',
        'last_name',
        'identificacao',
        'cpf'
    ]

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
            )
        }),
        ('Informações pessoais', {
            'fields': (
                'first_name',
                'last_name',
                'cpf',
                'data_nascimento',
                'identificacao',
                'tipo_usuario',
                'centro', # O campo 'estado' foi removido daqui
                'telefone',
            )
        }),
        ('Permissões', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Datas importantes', {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'cpf',
                'tipo_usuario',
                'centro', # O campo 'estado' foi removido daqui
                'password1',
                'password2',
            ),
        }),
    )