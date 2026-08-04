from django import forms
from .models import Formulario, Pergunta, OpcaoPergunta, RegraPulo

class FormularioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = ['nome', 'descricao', 'parte', 'tempo_estimado', 'ordem', 'ativo']


class PerguntaForm(forms.ModelForm):
    class Meta:
        model = Pergunta
        fields = ['titulo', 'subtitulo', 'tipo', 'obrigatoria', 'ordem', 'imagem_ilustrativa']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ordem'].required = False
        
        # Esconde o campo "ordem" se for uma pergunta nova
        if not self.instance.pk:
            self.fields['ordem'].widget = forms.HiddenInput()

class OpcaoForm(forms.ModelForm):
    class Meta:
        model = OpcaoPergunta
        fields = ['texto', 'ordem']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ordem'].required = False
        
        # Esconde o campo "ordem" se for uma opção nova
        if not self.instance.pk:
            self.fields['ordem'].widget = forms.HiddenInput()


class RegraPuloForm(forms.ModelForm):
    class Meta:
        model = RegraPulo
        # MODIFICADO: Adicionado 'acao' na lista de fields
        fields = ['opcao_condicao', 'acao', 'pergunta_destino']

    def __init__(self, *args, **kwargs):
        pergunta_origem = kwargs.pop('pergunta_origem', None)
        super().__init__(*args, **kwargs)
        if pergunta_origem:
            self.fields['opcao_condicao'].queryset = pergunta_origem.opcoes.all()
            self.fields['pergunta_destino'].queryset = Pergunta.objects.filter(
                formulario=pergunta_origem.formulario,
                ordem__gt=pergunta_origem.ordem
            )
            # NOVO: Retira a obrigatoriedade nativa do formulário
            self.fields['pergunta_destino'].required = False

    # NOVO: Validação que verifica a regra escolhida
    def clean(self):
        cleaned_data = super().clean()
        acao = cleaned_data.get('acao')
        pergunta_destino = cleaned_data.get('pergunta_destino')
        
        # Só exige uma pergunta de destino se a ação for realmente 'pular'
        if acao == 'pular' and not pergunta_destino:
            self.add_error('pergunta_destino', 'Você deve selecionar uma pergunta de destino para pular.')
            
        return cleaned_data