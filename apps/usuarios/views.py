from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario
from .forms import UsuarioForm

from .decorators import perfil_obrigatorio


def login_view(request):
    if request.user.is_authenticated:
        return _redirecionar_por_perfil(request)

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        manter_conectado = request.POST.get('manter_conectado')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if manter_conectado:
                # Mantém sessão por 14 dias mesmo fechando o navegador
                request.session.set_expiry(60 * 60 * 24 * 14)
            else:
                # Expira quando o navegador for fechado
                request.session.set_expiry(0)
            return _redirecionar_por_perfil(request)

        messages.error(request, 'E-mail ou senha inválidos.')
        return render(request, 'login.html', {'email': email})

    return render(request, 'login.html')


def _redirecionar_por_perfil(request):
    """Redireciona o usuário para o dashboard correto conforme seu perfil."""
    user = request.user

    if user.is_superuser:
        return redirect('escolha_acesso')

    destinos = {
        'ADM': 'dashboard_adm',
        'PES': 'dashboard_pes',
        'ATE': 'dashboard_ate',
        'PAC': 'dashboard_pac',
    }
    destino = destinos.get(user.tipo_usuario)

    if not destino:
        messages.error(request, 'Perfil de usuário não reconhecido. Contate o administrador.')
        logout(request)
        return redirect('login')

    return redirect(destino)


@perfil_obrigatorio('ADM')
def dashboard_adm_view(request):
    return render(request, 'dashboard.html')


@perfil_obrigatorio('PES')
def dashboard_pes_view(request):
    return render(request, 'dashboard.html')


@perfil_obrigatorio('ATE')
def dashboard_ate_view(request):
    return render(request, 'dashboard.html')


@perfil_obrigatorio('PAC')
def dashboard_pac_view(request):
    return render(request, 'dashboard.html')


def escolha_acesso_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')
    return render(request, 'escolha_acesso.html', {'user': request.user})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


def timeout_view(request):
    return render(request, 'timeout.html')



@login_required
def listar_usuarios(request):

    usuarios = Usuario.objects.all().order_by(
        'first_name'
    )

    return render(
        request,
        'listar_usuarios.html',
        {
            'usuarios': usuarios
        }
    )


# Registrar um usuário
def registrar_usuario(request):
    
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid(): 
            usuario = form.save(commit=False)        
            usuario.is_active = False
            usuario.set_unusable_password()
            usuario.save()
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('listar_usuarios')
        else:
            messages.error(request, 'Erro no registro. Verifique os dados e tente novamente.')
            form = UsuarioForm()
        return render(request, 'registrar_usuario.html', {'form': form})

@login_required
def editar_usuario(request, usuario_id):

    if not request.user.is_superuser:
        messages.error(
            request,
            'Você não possui permissão.'
        )
        return redirect('listar_usuarios')

    usuario = get_object_or_404(
        Usuario,
        id=usuario_id
    )

    if request.method == 'POST':

        form = UsuarioForm(
            request.POST,
            instance=usuario
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Usuário atualizado com sucesso.'
            )

            return redirect(
                'listar_usuarios'
            )

    else:

        form = UsuarioForm(
            instance=usuario
        )

    return render(
        request,
        'editar_usuario.html',
        {
            'form': form,
            'usuario': usuario
        }
    )
