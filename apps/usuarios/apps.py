from django.apps import AppConfig


PERMISSOES_POR_GRUPO = {
    'Administrador Central': [
        'cadastrar_paciente',
        'visualizar_paciente',
        'buscar_paciente',
        'acompanhar_progresso',
        'agendar_atendimento',
        'aplicar_parte1',
        'aplicar_parte2',
        'editar_resposta',
        'registrar_exame',
        'registrar_atividade',
        'gerenciar_usuarios',
        'gerenciar_centros',
        'visualizar_auditoria',
    ],
    'Atendimento': [
        'cadastrar_paciente',
        'visualizar_paciente',
        'buscar_paciente',
        'acompanhar_progresso',
        'agendar_atendimento',
        'aplicar_parte1',
    ],
    'Pesquisador': [
        'visualizar_paciente',
        'buscar_paciente',
        'acompanhar_progresso',
        'aplicar_parte1',
        'aplicar_parte2',
        'editar_resposta',
        'registrar_exame',
        'registrar_atividade',
    ],
    'Paciente': [],
}


def atribuir_permissoes_aos_grupos(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    for nome_grupo, codenames in PERMISSOES_POR_GRUPO.items():
        grupo, _ = Group.objects.get_or_create(name=nome_grupo)

        if codenames:
            permissoes = Permission.objects.filter(
                content_type__app_label='usuarios',
                codename__in=codenames,
            )
            grupo.permissions.set(permissoes)


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.usuarios'
