from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
