from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from .forms import UsuarioForm
from .models import Usuario


class ForcarResetSenhaForm(PasswordResetForm):
    """
    Permite que usuários recém-criados (com senha inutilizável)
    também recebam o e-mail de criação de senha.
    """
    def get_users(self, email):
        return Usuario.objects.filter(
            email__iexact=email, 
            is_active=True
        )


def login_view(request):
    "Realiza login do usuário e redireciona para o dashboard."
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=email,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'E-mail ou senha inválidos.')

    return render(request, 'login.html')


def logout_view(request):
    "Realiza logout do usuário e redireciona para a página de login."
    logout(request)
    return redirect('login')


def timeout_view(request):
    "Exibe uma página de timeout quando a sessão expira."
    return render(request, 'timeout.html')


@login_required
def listar_usuarios(request):
    """
    Lista os usuários do sistema com base no nível de acesso.
    TI vê todos, ADM vê apenas os do seu centro.
    """
    
    # 1. Se for o TI (Superusuário): Enxerga TODOS os usuários de TODOS os centros
    if request.user.is_superuser:
        usuarios = Usuario.objects.all().order_by('first_name')
        
    # 2. Se for o ADM Central: Enxerga APENAS os usuários que têm o mesmo centro que ele
    elif request.user.tipo_usuario == 'ADM':
        usuarios = Usuario.objects.filter(centro=request.user.centro).order_by('first_name')
        
    # 3. Pesquisadores e Atendentes: Por segurança, só veem a si mesmos na tabela
    else:
        usuarios = Usuario.objects.filter(id=request.user.id)

    return render(
        request,
        'listar_usuarios.html',
        {
            'usuarios': usuarios
        }
    )


@login_required
def registrar_usuario(request):
    """
    Permite que administradores registrem novos 
    usuários no sistema e enviem um e-mail para 
    criação de senha.
    """
    # 1. Proteção de segurança
    if not (request.user.is_superuser or request.user.tipo_usuario == 'ADM'):
        messages.error(request, 'Você não possui permissão para cadastrar usuários.')
        return redirect('listar_usuarios')

    if request.method == "POST":
        form = UsuarioForm(request.POST, user_logado=request.user)

        if form.is_valid(): 
            usuario = form.save(commit=False)
            usuario.is_active = True 
            usuario.set_unusable_password()
            usuario.save()

            # 2. Geração da chave e do link
            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            token = default_token_generator.make_token(usuario)
            link_painel = request.build_absolute_uri(f'/contas/reset/{uid}/{token}/')

            assunto = 'IARA-Saúde: Acesso ao Sistema'
            mensagem = f"""Olá, {usuario.first_name}.

Seu cadastro na equipe do IARA-SAÚDE foi realizado com sucesso.
Para realizar o seu primeiro acesso, clique no link abaixo para criar a sua senha:
{link_painel}

Este link é seguro e de uso único.
"""
            # 3. Disparo de e-mail com Try/Except
            try:
                send_mail(
                    subject=assunto,
                    message=mensagem,
                    from_email='sistema@iarasaude.com.br', # Troque pelo seu DEFAULT_FROM_EMAIL depois se preferir
                    recipient_list=[usuario.email],
                    fail_silently=False,
                )
                messages.success(request, f'Usuário {usuario.first_name} cadastrado e e-mail enviado com sucesso!')
            except Exception as e:
                messages.warning(request, f'Usuário salvo no sistema, mas ocorreu um erro ao enviar o e-mail: {e}')
 
            # Retorna para a lista após salvar com sucesso
            return redirect('listar_usuarios')

        else:
            # Se o form for INVÁLIDO, ele entra aqui e exibe o erro
            messages.error(request, 'Erro no registro. Verifique os dados e tente novamente.')
    
    else:
        form = UsuarioForm(user_logado=request.user)
    return render(
        request, 
        'registrar_usuario.html', 
        {
            'form': form
        }
    )


@login_required
def editar_usuario(request, usuario_id):
    "Permite que administradores editem informações de usuários existentes no sistema."
    # Proteção: Apenas ADM Central ou TI podem editar
    if not (request.user.is_superuser or request.user.tipo_usuario == 'ADM'):
        messages.error(request, 'Você não possui permissão para editar usuários.')
        return redirect('listar_usuarios')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario, user_logado=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso.')
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario, user_logado=request.user)

    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})


@login_required
def excluir_usuario(request, usuario_id):
    "Permite que administradores excluam usuários do sistema."

    if not request.user.is_superuser:
        messages.error(request, 'Você não possui permissão para excluir usuários.')
        return redirect('listar_usuarios')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Proteção extra: O administrador não pode excluir a si mesmo acidentalmente
    if request.user == usuario:
        messages.error(request, 'Você não pode excluir sua própria conta.')
        return redirect('listar_usuarios')

    if request.method == 'POST':
        nome_deletado = f"{usuario.first_name} {usuario.last_name}"
        usuario.delete()
        messages.success(request, f'O acesso de {nome_deletado} foi removido permanentemente.')

    return redirect('listar_usuarios')

class CustomPasswordResetView(PasswordResetView):
    """
    Exibe a tela para o usuário digitar o e-mail.
    Após o envio, renderiza a mesma tela exibindo a mensagem de sucesso,
    sem precisar redirecionar para uma URL diferente.
    """
    template_name = 'resetar_senha.html'
    success_url = reverse_lazy('login') # Apenas para o Django não dar erro de rota ausente

    def form_valid(self, form):
        # 1. Faz o Django disparar o e-mail de reset padrão com o link
        super().form_valid(form)
        
        # 2. Renderiza a mesma tela enviando a variável 'sucesso' como True
        return render(self.request, self.template_name, {'sucesso': True})
    
class CriarSenhaView(PasswordResetConfirmView):
    "View para criação de senha após o primeiro acesso do usuário."

    template_name = 'criar_senha.html'

    def form_valid(self, form):
        # 1. Salva a nova senha no banco de dados
        form.save()

        # 2. Ao invés de redirecionar para outra URL, renderiza a mesma tela, 
        # mas passando uma variável chamada 'sucesso'
        return render(self.request, self.template_name, {'sucesso': True})