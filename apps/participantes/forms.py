from django import forms
from .models import Participante


class ParticipanteForm(forms.ModelForm):

    class Meta:
        model = Participante

        fields = [
            'nome',
            'email',
            'data_nascimento',
            'sexo',
            'estado',
            'centro',
            'telefone',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3',
                'placeholder': 'Nome completo'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3',
                'placeholder': 'E-mail do participante'
            }),

            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3'
            }),

            'sexo': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3'
            }),

            'estado': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3'
            }),

            'centro': forms.NumberInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3',
                'placeholder': 'Ex: 01'
            }),

            'telefone': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3',
                'placeholder': '(DD) 90000-0000'
            }),
        }