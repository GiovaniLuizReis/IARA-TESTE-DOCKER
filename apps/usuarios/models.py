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

    def __str__(self):
        return (
            f'{self.first_name} '
            f'{self.last_name}'
        )