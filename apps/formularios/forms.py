from django import forms
from .models import Formulario, Bloco, Pergunta, OpcaoPergunta, RegraPulo

class FormularioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = ['nome', 'descricao', 'ativo', 'publicado']

class BlocoForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = ['titulo', 'ordem', 'tempo_estimado']

class PerguntaForm(forms.ModelForm):
    class Meta:
        model = Pergunta
        fields = ['titulo', 'subtitulo', 'tipo', 'obrigatoria', 'ordem']

class OpcaoForm(forms.ModelForm):
    class Meta:
        model = OpcaoPergunta
        fields = ['texto', 'ordem']

class RegraPuloForm(forms.ModelForm):
    class Meta:
        model = RegraPulo
        fields = ['opcao_condicao', 'pergunta_destino']

    def __init__(self, *args, **kwargs):
        pergunta_origem = kwargs.pop('pergunta_origem', None)
        super().__init__(*args, **kwargs)
        if pergunta_origem:
            self.fields['opcao_condicao'].queryset = OpcaoPergunta.objects.filter(pergunta=pergunta_origem)
            # Evita loops direcionando apenas para perguntas de blocos posteriores ou ordens futuras
            self.fields['pergunta_destino'].queryset = Pergunta.objects.filter(
                bloco__formulario=pergunta_origem.bloco.formulario
            ).exclude(id=pergunta_origem.id)