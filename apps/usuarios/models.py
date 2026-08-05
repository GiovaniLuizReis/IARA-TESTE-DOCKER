from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    "classe para gerenciar a criação de usuários e superusuários"

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

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            email,
            password,
            **extra_fields
        )


class CentroInvestigacao(models.Model):
    """Modelo para armazenar as unidades/centros de cada estado"""
    
    ESTADOS_PESQUISA = (
        ('AC', 'Acre'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('PA', 'Pará'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('TO', 'Tocantins'),
    )

    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=ESTADOS_PESQUISA)
    numero = models.IntegerField()

    class Meta:
        verbose_name = 'Centro de Investigação'
        verbose_name_plural = 'Centros de Investigação'
        unique_together = ['estado', 'numero']

    def __str__(self):
        return f"{self.get_estado_display()} - {self.nome}" # pylint: disable=no-member


class Usuario(AbstractUser):

    username = None
    objects = UsuarioManager()
    
    TIPO_USUARIO = (
        ('ADM', 'Administrador Central'),
        ('PES', 'Pesquisador'),
        ('ATE', 'Atendimento'),
    )

    email = models.EmailField(
        unique=True
    )

    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='CPF',
        blank=True,
        null=True 
    )

    data_nascimento = models.DateField(
        verbose_name='Data de Nascimento',
        blank=True,
        null=True
    )
    
    # Campo retornado para evitar o erro no makemigrations e admin
    identificacao = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    tipo_usuario = models.CharField(
        max_length=3,
        choices=TIPO_USUARIO
    )

    centro = models.ForeignKey(
        CentroInvestigacao, 
        on_delete=models.PROTECT, 
        related_name='usuarios',
        null=True,
        blank=True
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'

    # Ajustado para facilitar a criação de superusuário pelo terminal
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'tipo_usuario'
    ]

    def save(self, *args, **kwargs):
        # Gera a identificação automaticamente baseada no Centro vinculado
        if not self.identificacao and self.centro:
            ultimo = Usuario.objects.filter(
                centro=self.centro,
                tipo_usuario=self.tipo_usuario
            ).count() + 1

            sequencial = str(ultimo).zfill(5)
            estado_sigla = self.centro.estado # pylint: disable=no-member
            centro_num = str(self.centro.numero).zfill(2) # pylint: disable=no-member

            self.identificacao = (
                f'{estado_sigla}'
                f'{centro_num}'
                f'{self.tipo_usuario}'
                f'{sequencial}'
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'