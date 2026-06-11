from django.db import models


class Paciente(models.Model):

    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
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

    estado = models.CharField(
        max_length=2,
        choices=ESTADOS
    )

    centro = models.IntegerField()

    identificacao = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    nome = models.CharField(
        max_length=200
    )

    email = models.EmailField()

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    data_nascimento = models.DateField()

    sexo = models.CharField(
        max_length=1,
        choices=SEXO
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.identificacao:

            ultimo = Paciente.objects.filter(
                estado=self.estado,
                centro=self.centro
            ).count() + 1

            sequencial = str(ultimo).zfill(5)

            centro = str(self.centro).zfill(2)

            self.identificacao = (
                f'{self.estado}'
                f'{centro}'
                f'PAC'
                f'{sequencial}'
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome