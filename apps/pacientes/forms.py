from django import forms
from .models import Paciente


class PacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente

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
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3'
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
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3'
            }),

            'telefone': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3'
            }),
        }