import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.participantes.models import Participante
from apps.formularios.models import Formulario, Pergunta, OpcaoPergunta

User = get_user_model()

class Atividade(models.Model):
    STATUS_CHOICES = (
        ('nao_iniciado', 'Não Iniciado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
    )
    
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='atividades')
    formulario = models.ForeignKey(Formulario, on_delete=models.PROTECT)
    
    token_acesso = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_iniciado')
    progresso_percentual = models.IntegerField(default=0)

    ultima_pergunta_acessada = models.ForeignKey(
        'formularios.Pergunta', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='+'
    )
    
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    tempo_gasto_segundos = models.IntegerField(default=0)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.participante.nome} - {self.formulario.nome}"

class Resposta(models.Model):
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='respostas')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    valor_texto = models.TextField(blank=True, null=True)
    opcoes_selecionadas = models.ManyToManyField(OpcaoPergunta, blank=True)
    respondida_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('atividade', 'pergunta')

class HistoricoAtividade(models.Model):
    ORIGEM_CHOICES = (('online', 'Online'), ('papel', 'Papel'))
    TIPO_ACAO_CHOICES = (
        ('inicio', 'Início de Preenchimento'),
        ('pausa', 'Pausa/Interrupção'),
        ('retomada', 'Retomada de Preenchimento'),
        ('conclusao', 'Conclusão do Formulário'),
        ('assumir', 'Pesquisador Assumiu'),
        ('alteracao', 'Alteração de Resposta'),
        ('outros', 'Outros Eventos')
    )
    
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='historico')
    tipo_acao = models.CharField(max_length=20, choices=TIPO_ACAO_CHOICES, default='outros')
    acao = models.CharField(max_length=255)
    usuario_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    origem = models.CharField(max_length=20, choices=ORIGEM_CHOICES, default='online')
    data_hora = models.DateTimeField(auto_now_add=True)
    detalhes_json = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['data_hora']

    def __str__(self):
        return f"{self.data_hora.strftime('%d/%m/%Y %H:%M')} - {self.get_tipo_acao_display()} - {self.atividade}"