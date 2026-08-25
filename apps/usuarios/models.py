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
    """Modelo para armazenar as unidades/centros numéricos de cada estado conforme protocolo IARA"""
    
    # Estados numerados de 1 a 9 conforme o PDF IARA-Saúde
    ESTADOS_PESQUISA = (
        ('1', 'Acre'),
        ('2', 'Amapá'),
        ('3', 'Amazonas'),
        ('4', 'Maranhão'),
        ('5', 'Mato Grosso'),
        ('6', 'Pará'),
        ('7', 'Rondônia'),
        ('8', 'Roraima'),
        ('9', 'Tocantins'),
    )

    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, choices=ESTADOS_PESQUISA)
    numero = models.IntegerField()

    class Meta:
        verbose_name = 'Centro de Investigação'
        verbose_name_plural = 'Centros de Investigação'
        unique_together = ['estado', 'numero']

    def __str__(self):
        return f"{self.get_estado_display()} (CI: {self.numero}) - {self.nome}" # pylint: disable=no-member


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

    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'tipo_usuario'
    ]

    def save(self, *args, **kwargs):
        if not self.identificacao and self.centro:
            ultimo = Usuario.objects.filter(
                centro=self.centro,
                tipo_usuario=self.tipo_usuario
            ).count() + 1

            # Formato de 4 casas decimais para o sequencial
            sequencial = str(ultimo).zfill(4)
            estado_num = self.centro.estado # pylint: disable=no-member
            centro_num = str(self.centro.numero) # pylint: disable=no-member

            # ID do Usuário: Estado + CI + Tipo (ADM/PES) + Sequencial (Ex: 11ADM0001)
            self.identificacao = (
                f'{estado_num}'
                f'{centro_num}'
                f'{self.tipo_usuario}'
                f'{sequencial}'
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'