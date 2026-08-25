from django import forms
from .models import Participante

class ParticipanteForm(forms.ModelForm):

    class Meta:
        model = Participante
        fields = [
            'nome',
            'sobrenome',
            'cpf',
            'data_nascimento',
            'nome_mae',
            'email',
            'telefone',
            'sexo',
            'cep',
            'endereco',
            'numero_endereço',
            'complemento',
            'situacao_trabalho',
            'tipo_vinculo',
            'instituicao_vinculo',
            'centro',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500',
                'placeholder': 'Nome'
            }),
            'sobrenome': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500',
                'placeholder': 'Sobrenome'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500',
                'placeholder': '000.000.000-00'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500'
            }),
            'nome_mae': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500',
                'placeholder': 'Nome completo da mãe'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500',
                'placeholder': 'E-mail do participante'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500',
                'placeholder': '(DD) 90000-0000'
            }),
            
            'sexo': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500 bg-white'
            }),
           
            'cep': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500',
                'placeholder': '00000-000'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500',
                'placeholder': 'Ex: Rua Principal, 123 - Bairro'
            }),
            'numero_endereço': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500',
                'placeholder': 'Número do endereço'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500',
                'placeholder': 'Apto, Bloco, Casa (Opcional)'
            }),
            'situacao_trabalho': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500 bg-white'
            }),
            'tipo_vinculo': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500 bg-white'
            }),
            'instituicao_vinculo': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500',
                'placeholder': 'Ex: Ministério da Saúde, Hospital X...'
            }),
            'centro': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500 bg-white'
            }),
        }