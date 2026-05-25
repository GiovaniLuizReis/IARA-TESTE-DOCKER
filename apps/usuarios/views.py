from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


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


def dashboard_view(request):
    return render(request, 'dashboard.html')


def timeout_view(request):
    return render(request, 'timeout.html')

