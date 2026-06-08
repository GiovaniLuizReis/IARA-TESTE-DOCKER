import uuid
from django.db import models

class Formulario(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    publicado = models.BooleanField(default=False) # Adicionado controle de publicação
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Bloco(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE, related_name='blocos')
    titulo = models.CharField(max_length=200)
    ordem = models.IntegerField(default=1)
    tempo_estimado = models.IntegerField(default=5)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.titulo

class Pergunta(models.Model):
    TIPOS = (
        ('texto', 'Texto'),
        ('numero', 'Número'),
        ('data', 'Data'),
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
        ('select', 'Select'),
        ('rating', 'Rating (Estrelas)'),
        ('nps', 'NPS (0 a 10)'),
        ('matrix', 'Matriz'),
        ('ranking', 'Ranking'),
    )

    bloco = models.ForeignKey(Bloco, on_delete=models.CASCADE, related_name='perguntas')
    titulo = models.TextField()
    subtitulo = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    obrigatoria = models.BooleanField(default=True)
    ordem = models.IntegerField(default=1)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.titulo

class OpcaoPergunta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='opcoes')
    texto = models.CharField(max_length=200)
    ordem = models.IntegerField(default=1)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.texto

class RegraPulo(models.Model):
    pergunta_origem = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='regras_origem')
    opcao_condicao = models.ForeignKey(OpcaoPergunta, on_delete=models.CASCADE, null=True, blank=True)
    pergunta_destino = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='regras_destino')
    
    def __str__(self):
        return f"Se {self.pergunta_origem} == {self.opcao_condicao} -> Pula para {self.pergunta_destino}"

class Coleta(models.Model):
    STATUS_CHOICES = (
        ('planejada', 'Planejada'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
    )
    formulario = models.ForeignKey(Formulario, on_delete=models.PROTECT, related_name='coletas')
    nome = models.CharField(max_length=200)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejada')

    def __str__(self):
        return self.nome

class SessaoPaciente(models.Model):
    coleta = models.ForeignKey(Coleta, on_delete=models.CASCADE, related_name='sessoes')
    token_acesso = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email_paciente = models.EmailField() # Assumindo que o token vai por email
    iniciada_em = models.DateTimeField(null=True, blank=True)
    ultima_interacao = models.DateTimeField(auto_now=True)
    concluida = models.BooleanField(default=False)
    bloco_atual = models.ForeignKey(Bloco, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.email_paciente} - {self.coleta.nome}"

class Resposta(models.Model):
    sessao = models.ForeignKey(SessaoPaciente, on_delete=models.CASCADE, related_name='respostas')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    valor_texto = models.TextField(blank=True, null=True)
    opcoes_selecionadas = models.ManyToManyField(OpcaoPergunta, blank=True)
    respondida_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sessao', 'pergunta')