from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsuarioManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('O email é obrigatório')

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email,
        password=None,
        **extra_fields
    ):

        extra_fields.setdefault(
            'is_staff',
            True
        )

        extra_fields.setdefault(
            'is_superuser',
            True
        )

        extra_fields.setdefault(
            'is_active',
            True
        )

        return self.create_user(
            email,
            password,
            **extra_fields
        )
    
class Usuario(AbstractUser):

    username = None
    objects = UsuarioManager()

    TIPO_USUARIO = (
        ('ADM', 'Administrador Central'),
        ('PES', 'Pesquisador'),
        ('PAC', 'Paciente'),
        ('ATE', 'Atendimento'),
    )

    ESTADOS = (
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('MG', 'Minas Gerais'),
        ('PE', 'Pernambuco'),
        ('PR', 'Paraná'),
        ('RJ', 'Rio de Janeiro'),
        ('RS', 'Rio Grande do Sul'),
        ('SP', 'São Paulo'),
    )

    email = models.EmailField(
        unique=True
    )

    identificacao = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    tipo_usuario = models.CharField(
        max_length=3,
        choices=TIPO_USUARIO
    )

    estado = models.CharField(
        max_length=2,
        choices=ESTADOS
    )

    centro = models.IntegerField()

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'tipo_usuario',
        'estado',
        'centro'
    ]

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        permissions = [
            ('cadastrar_paciente',  'Pode cadastrar paciente'),
            ('visualizar_paciente', 'Pode visualizar dados do paciente'),
            ('buscar_paciente',     'Pode buscar paciente'),
            ('acompanhar_progresso','Pode acompanhar progresso do paciente'),
            ('agendar_atendimento', 'Pode agendar atendimento presencial'),
            ('aplicar_parte1',      'Pode aplicar Parte 1 do questionário'),
            ('aplicar_parte2',      'Pode aplicar Parte 2 do questionário'),
            ('editar_resposta',     'Pode editar resposta (registra auditoria)'),
            ('registrar_exame',     'Pode registrar exame'),
            ('registrar_atividade', 'Pode registrar atividade'),
            ('gerenciar_usuarios',  'Pode criar e gerenciar usuários'),
            ('gerenciar_centros',   'Pode gerenciar centros de pesquisa'),
            ('visualizar_auditoria','Pode visualizar histórico de alterações'),
        ]

    def save(self, *args, **kwargs):

        if not self.identificacao:

            ultimo = Usuario.objects.filter(
                estado=self.estado,
                centro=self.centro,
                tipo_usuario=self.tipo_usuario
            ).count() + 1

            sequencial = str(ultimo).zfill(5)

            centro = str(self.centro).zfill(2)

            self.identificacao = (
                f'{self.estado}'
                f'{centro}'
                f'{self.tipo_usuario}'
                f'{sequencial}'
            )

        super().save(*args, **kwargs)
        self._atribuir_grupo()

    def _atribuir_grupo(self):
        from django.contrib.auth.models import Group

        GRUPOS = {
            'ADM': 'Administrador Central',
            'ATE': 'Atendimento',
            'PES': 'Pesquisador',
            'PAC': 'Paciente',
        }

        nome_grupo = GRUPOS.get(self.tipo_usuario)
        if not nome_grupo:
            return

        try:
            grupo = Group.objects.get(name=nome_grupo)
        except Group.DoesNotExist:
            return

        grupos_iara = Group.objects.filter(name__in=GRUPOS.values())
        self.groups.remove(*grupos_iara)
        self.groups.add(grupo)

    def __str__(self):
        return (
            f'{self.first_name} '
            f'{self.last_name}'
        )