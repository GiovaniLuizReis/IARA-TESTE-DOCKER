from django.db import models

class Formulario(models.Model):
    PARTE_CHOICES = (
        ('P1', 'Parte 1 - Online (Paciente)'),
        ('P2', 'Parte 2 - Presencial (Laboratório)'),
    )
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    parte = models.CharField(max_length=2, choices=PARTE_CHOICES, default='P1')
    tempo_estimado = models.IntegerField(default=5, help_text="Tempo médio estimado em minutos")
    ordem = models.IntegerField(default=1, help_text="Ordem de exibição no painel")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.get_parte_display()})"


class Pergunta(models.Model):
    TIPO_CHOICES = (
        ('texto', 'Texto Livre'),
        ('numero', 'Número'),
        ('data', 'Data'),
        ('radio', 'Seleção Única (Radio)'),
        ('checkbox', 'Múltipla Escolha (Checkbox)'),
        ('select', 'Menu Suspenso (Select)'),
        ('rating', 'Avaliação (Rating)'),
        ('nps', 'NPS (0-10)'),
        ('matrix', 'Matriz de Opções'),
        ('ranking', 'Ordenação (Ranking)'),
    )
    
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE, related_name='perguntas')
    titulo = models.CharField(max_length=500)
    subtitulo = models.CharField(max_length=500, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='texto')
    obrigatoria = models.BooleanField(default=True)
    ordem = models.IntegerField(default=1)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"{self.formulario.nome} - {self.titulo[:50]}"


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
    opcao_condicao = models.ForeignKey(OpcaoPergunta, on_delete=models.CASCADE, related_name='regras_condicao')
    pergunta_destino = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='regras_destino')

    def __str__(self):
        return f"Se '{self.opcao_condicao.texto}' -> Pular para '{self.pergunta_destino.titulo[:30]}'"