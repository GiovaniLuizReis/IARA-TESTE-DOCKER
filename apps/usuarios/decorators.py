from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def perfil_obrigatorio(*tipos):
    """
    Decorator que verifica autenticação e restringe acesso por tipo_usuario.
    Superusuários têm acesso irrestrito.

    Uso:
        @perfil_obrigatorio('ADM')
        @perfil_obrigatorio('PES', 'ADM')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.is_superuser or request.user.tipo_usuario in tipos:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('login')
        return wrapper
    return decorator
