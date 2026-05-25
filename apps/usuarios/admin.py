from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    ordering = ['email']

    list_display = [
        'email',
        'first_name',
        'last_name',
        'identificacao',
        'tipo_usuario',
        'estado',
        'centro',
        'is_staff',
    ]

    search_fields = [
        'email',
        'first_name',
        'last_name',
        'identificacao'
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
                'identificacao',
                'tipo_usuario',
                'estado',
                'centro',
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
                'tipo_usuario',
                'estado',
                'centro',
                'password1',
                'password2',
            ),
        }),
    )