from django.db import models
from apps.usuarios.models import CentroInvestigacao 

class Participante(models.Model):

    SITUACAO_CHOICES = (
        ('ativo', 'Ativo'),
        ('aposentado', 'Aposentado'),
    )

    VINCULO_CHOICES = (
        ('servidor', 'Servidor'),
        ('terceirizado', 'Terceirizado'),
    )

    centro = models.ForeignKey(
        CentroInvestigacao, 
        on_delete=models.PROTECT, 
        related_name='participantes'
    )
    
    identificacao = models.CharField(max_length=30, unique=True, blank=True)

    # NOME SEPARADO AQUI
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200)
    
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    nome_mae = models.CharField(max_length=255)
    email = models.EmailField()
    situacao_trabalho = models.CharField(max_length=20, choices=SITUACAO_CHOICES)
    tipo_vinculo = models.CharField(max_length=20, choices=VINCULO_CHOICES)
    instituicao_vinculo = models.CharField(max_length=255)

    telefone = models.CharField(max_length=20, blank=True, null=True)

    cep = models.CharField(max_length=9, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.identificacao and self.centro:
            ultimo = Participante.objects.filter(
                centro=self.centro
            ).count() + 1

            sequencial = str(ultimo).zfill(5)
            
            estado_sigla = self.centro.estado
            centro_num = str(self.centro.numero).zfill(2)

            self.identificacao = (
                f'{estado_sigla}'
                f'{centro_num}'
                f'PAC'
                f'{sequencial}'
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'