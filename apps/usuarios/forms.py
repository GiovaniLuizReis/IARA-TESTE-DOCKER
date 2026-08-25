from django import forms
from django.contrib.auth.forms import AuthenticationForm
from apps.usuarios.models import Usuario, CentroInvestigacao

class LoginForm(AuthenticationForm):
    "Autenticação de usuário via e-mail e senha"
    username = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu e-mail',
            'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500'
        })
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
            'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500'
        })
    )


class UsuarioForm(forms.ModelForm):
    "Formulário para criação e edição de usuários"

    # Campo apenas para a tela (não é salvo no banco), usado para o JavaScript filtrar as unidades
    estado_filtro = forms.ChoiceField(
        choices=[('', 'Selecione um Estado')] + list(CentroInvestigacao.ESTADOS_PESQUISA),
        label="Estado da Unidade",
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500 bg-white'
        })
    )

    class Meta:
        "classe Meta do formulário"
        model = Usuario
        fields = [
            'first_name',
            'last_name',
            'cpf',
            'data_nascimento',
            'email',
            'telefone',
            'tipo_usuario',
            'estado_filtro',
            'centro',
            'is_active',
            'is_staff',
            'is_superuser',
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500'}),
            'cpf': forms.TextInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500'}),
            'telefone': forms.TextInput(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500'}),
            'tipo_usuario': forms.Select(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500 bg-white'}),
            'centro': forms.Select(attrs={'class': 'w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500 bg-white'}),
            
            # Ajuste visual moderno para os checkboxes
            'is_active': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-emerald-600 bg-gray-100 border-gray-300 rounded focus:ring-emerald-500 focus:ring-2'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-emerald-600 bg-gray-100 border-gray-300 rounded focus:ring-emerald-500 focus:ring-2'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-emerald-600 bg-gray-100 border-gray-300 rounded focus:ring-emerald-500 focus:ring-2'}),
        }

    def __init__(self, *args, **kwargs):
        # O 'pop' retira o user_logado antes do Django processar o resto e dar erro
        user_logado = kwargs.pop('user_logado', None)
        
        super().__init__(*args, **kwargs)

        # Ajusta os rótulos na tela
        self.fields['first_name'].label = 'Nome'
        self.fields['last_name'].label = 'Sobrenome'
        self.fields['cpf'].label = 'CPF'
        self.fields['data_nascimento'].label = 'Data de Nascimento'
        self.fields['email'].label = 'E-mail'
        self.fields['centro'].label = 'Unidade (Centro)'
        self.fields['centro'].empty_label = 'Escolha um estado primeiro...'
        
        self.fields['is_active'].label = 'Usuário Ativo (Pode fazer login)'
        self.fields['is_staff'].label = 'Acesso ao Painel Admin Django (Membro da Equipe)'
        self.fields['is_superuser'].label = 'Status de Superusuário (Acesso Total de TI)'

        # Coloca os placeholders individualmente
        self.fields['first_name'].widget.attrs['placeholder'] = 'Digite seu nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Digite seu sobrenome'
        self.fields['cpf'].widget.attrs['placeholder'] = '000.000.000-00'
        self.fields['data_nascimento'].widget.attrs['placeholder'] = 'dd/mm/aaaa'
        self.fields['email'].widget.attrs['placeholder'] = 'exemplo@email.com'
        self.fields['telefone'].widget.attrs['placeholder'] = '(99) 99999-9999'

        # Remove os campos se não for o TI
        if user_logado and not user_logado.is_superuser:
            if 'is_staff' in self.fields:
                del self.fields['is_staff']
            if 'is_superuser' in self.fields:
                del self.fields['is_superuser']