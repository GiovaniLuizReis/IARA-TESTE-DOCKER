from django.db import models

class Formulario(models.Model):
    PARTE_CHOICES = (
        ('P1', 'Parte 1 - Online (Paciente)'),
        ('P2', 'Parte 2 - Presencial (Laboratório)'),
    )
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    parte = models.CharField(max_length=2, choices=PARTE_CHOICES, default='P2')
    tempo_estimado = models.IntegerField(default=15, help_text="Tempo médio estimado em minutos")
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
        ('duracao', 'Duração (Horas e Minutos)'),
    )
    
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE, related_name='perguntas')
    titulo = models.CharField(max_length=500)
    subtitulo = models.CharField(max_length=500, blank=True, null=True)

    # Novo campo de imagem:
    imagem_ilustrativa = models.ImageField(upload_to='perguntas_imagens/', blank=True, null=True, help_text="Imagem opcional para ilustrar a escala ou o enunciado")

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='texto')
    obrigatoria = models.BooleanField(default=True)
    ordem = models.IntegerField(default=1)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"{self.formulario.nome} - {self.titulo[:50]}"

    # Auto-numera a pergunta com base no formulário
    def save(self, *args, **kwargs):
        if not self.pk and self.ordem == 1:
            ultima_pergunta = Pergunta.objects.filter(formulario=self.formulario).order_by('-ordem').first()
            if ultima_pergunta:
                self.ordem = ultima_pergunta.ordem + 1
        super().save(*args, **kwargs)


class OpcaoPergunta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='opcoes')
    texto = models.CharField(max_length=200)
    ordem = models.IntegerField(default=1)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.texto


    def save(self, *args, **kwargs):
        if not self.pk and self.ordem == 1:
            ultima_opcao = OpcaoPergunta.objects.filter(pergunta=self.pergunta).order_by('-ordem').first()
            if ultima_opcao:
                self.ordem = ultima_opcao.ordem + 1
        super().save(*args, **kwargs)


class RegraPulo(models.Model):
    ACAO_CHOICES = (
        ('pular', 'Pular para Pergunta Específica'),
        ('finalizar', 'Finalizar Questionário'),
    )
    
    pergunta_origem = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='regras_origem')
    opcao_condicao = models.ForeignKey(OpcaoPergunta, on_delete=models.CASCADE, related_name='regras_condicao')
    
    # NOVO CAMPO: Define a ação a ser tomada
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES, default='pular')
    
    # MODIFICADO: Adicionado blank=True, null=True para quando a ação for 'finalizar'
    pergunta_destino = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='regras_destino', blank=True, null=True)

    def __str__(self):
        if self.acao == 'finalizar':
            return f"Se '{self.opcao_condicao.texto}' -> Finalizar Questionário"
        # Se for para pular, garante que o destino existe antes de tentar ler o título para não dar erro
        destino = self.pergunta_destino.titulo[:30] if self.pergunta_destino else "Nenhum"
        return f"Se '{self.opcao_condicao.texto}' -> Pular para '{destino}'"