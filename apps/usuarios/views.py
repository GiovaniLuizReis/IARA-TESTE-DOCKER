from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Usuario
from .forms import UsuarioForm


def login_view(request):
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
    logout(request)
    return redirect('login')


def dashboard_view(request):
    return render(request, 'dashboard.html')


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