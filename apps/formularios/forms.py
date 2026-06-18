from django import forms
from .models import Formulario, Pergunta, OpcaoPergunta, RegraPulo

class FormularioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = ['nome', 'descricao', 'parte', 'tempo_estimado', 'ordem', 'ativo']


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
            self.fields['opcao_condicao'].queryset = pergunta_origem.opcoes.all()
            self.fields['pergunta_destino'].queryset = Pergunta.objects.filter(
                formulario=pergunta_origem.formulario,
                ordem__gt=pergunta_origem.ordem
            )