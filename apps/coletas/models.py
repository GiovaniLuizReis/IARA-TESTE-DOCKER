import uuid
from django.db import models
from apps.formularios.models import Formulario, Bloco, Pergunta, OpcaoPergunta

class Coleta(models.Model):
    STATUS_CHOICES = (
        ('planejada', 'Planejada'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
    )
    nome = models.CharField(max_length=200)
    formulario_parte1 = models.ForeignKey(Formulario, on_delete=models.PROTECT, related_name='coletas_p1')
    formulario_parte2 = models.ForeignKey(Formulario, on_delete=models.PROTECT, related_name='coletas_p2')
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejada')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class SessaoPaciente(models.Model):
    FASES_CHOICES = (
        ('parte1', 'Parte 1 - Online (Paciente)'),
        ('parte2', 'Parte 2 - Presencial (Laboratório)'),
        ('finalizado', 'Fluxo Concluído'),
    )
    ORIGEM_CHOICES = (
        ('paciente', 'Paciente (Remoto)'),
        ('pesquisador', 'Pesquisador (Presencial)'),
    )
    
    coleta = models.ForeignKey(Coleta, on_delete=models.CASCADE, related_name='sessoes')
    token_acesso = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email_paciente = models.EmailField()
    
    fase_atual = models.CharField(max_length=20, choices=FASES_CHOICES, default='parte1')
    formulario_atual = models.ForeignKey(Formulario, on_delete=models.SET_NULL, null=True, blank=True)
    bloco_atual = models.ForeignKey(Bloco, on_delete=models.SET_NULL, null=True, blank=True)
    
    preenchido_por = models.CharField(max_length=20, choices=ORIGEM_CHOICES, default='paciente')
    iniciada_em = models.DateTimeField(null=True, blank=True)
    ultima_interacao = models.DateTimeField(auto_now=True)
    concluida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email_paciente} - {self.coleta.nome} ({self.get_fase_atual_display()})"

class Resposta(models.Model):
    sessao = models.ForeignKey(SessaoPaciente, on_delete=models.CASCADE, related_name='respostas')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    valor_texto = models.TextField(blank=True, null=True)
    opcoes_selecionadas = models.ManyToManyField(OpcaoPergunta, blank=True)
    respondida_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sessao', 'pergunta')