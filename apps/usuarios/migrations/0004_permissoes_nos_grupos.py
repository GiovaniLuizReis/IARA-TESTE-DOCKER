from django.db import migrations

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
        'aplicar_parte2',
        'editar_resposta',
    ],
    'Pesquisador': [
        'visualizar_paciente',
        'buscar_paciente',
        'acompanhar_progresso',
        'registrar_exame',
        'registrar_atividade',
        'visualizar_auditoria',
    ],
    'Paciente': [],
}


def atribuir_permissoes(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    for nome_grupo, codenames in PERMISSOES_POR_GRUPO.items():
        try:
            grupo = Group.objects.get(name=nome_grupo)
        except Group.DoesNotExist:
            continue

        permissoes = Permission.objects.filter(codename__in=codenames)
        grupo.permissions.set(permissoes)


def remover_permissoes(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')

    for nome_grupo in PERMISSOES_POR_GRUPO:
        try:
            grupo = Group.objects.get(name=nome_grupo)
            grupo.permissions.clear()
        except Group.DoesNotExist:
            continue


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_grupos_e_permissoes'),
    ]

    operations = [
        migrations.RunPython(atribuir_permissoes, remover_permissoes),
    ]
