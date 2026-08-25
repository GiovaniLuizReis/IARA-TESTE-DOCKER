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
    
    SEXO_CHOICES = (
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('intersexo', 'Intersexo'),
    )

    centro = models.ForeignKey(
        CentroInvestigacao, 
        on_delete=models.PROTECT, 
        related_name='participantes'
    )
    
    identificacao = models.CharField(max_length=30, unique=True, blank=True)

    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200)
    
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    nome_mae = models.CharField(max_length=255)
    email = models.EmailField()
    situacao_trabalho = models.CharField(max_length=20, choices=SITUACAO_CHOICES)
    tipo_vinculo = models.CharField(max_length=20, choices=VINCULO_CHOICES)
    instituicao_vinculo = models.CharField(max_length=255)
    sexo = models.CharField(max_length=20, choices=SEXO_CHOICES, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    cep = models.CharField(max_length=9, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    numero_endereço = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.identificacao and self.centro:
            ultimo = Participante.objects.filter(
                centro=self.centro
            ).count() + 1

            # Participante não ultrapassa 4 casas decimais conforme o PDF
            sequencial = str(ultimo).zfill(4)
            
            estado_num = self.centro.estado
            centro_num = str(self.centro.numero)

            # Formação Exata do ID: Número do Estado + Número do CI + Sequencial 4 dígitos
            # Ex: 630001 (Pará, Marabá, Paciente 1)
            self.identificacao = (
                f'{estado_num}'
                f'{centro_num}'
                f'{sequencial}'
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'