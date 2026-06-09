from django.db import models

class Formulario(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    publicado = models.BooleanField(default=False)
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