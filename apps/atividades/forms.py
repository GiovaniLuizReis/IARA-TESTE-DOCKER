from django import forms
from .models import Coleta

class ColetaForm(forms.ModelForm):
    class Meta:
        model = Coleta
        fields = ['nome', 'formulario_parte1', 'formulario_parte2', 'data_inicio', 'data_fim', 'status']