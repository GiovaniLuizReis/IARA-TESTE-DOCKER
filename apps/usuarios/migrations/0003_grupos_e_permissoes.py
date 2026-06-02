from django.db import migrations

NOMES_GRUPOS = [
    'Administrador Central',
    'Atendimento',
    'Pesquisador',
    'Paciente',
]


def criar_grupos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    for nome in NOMES_GRUPOS:
        Group.objects.get_or_create(name=nome)


def remover_grupos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=NOMES_GRUPOS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_permissoes_customizadas'),
    ]

    operations = [
        migrations.RunPython(criar_grupos, remover_grupos),
    ]
