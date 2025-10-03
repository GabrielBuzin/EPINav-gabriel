from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages



def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('usuario_id') or request.session.get('colaborador_id'):
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Checa se é um usuário do sistema ou colaborador logado
        is_admin = request.session.get('is_admin', False)  # para usuariosSistema
        usuario_id = request.session.get('usuario_id')
        
        if usuario_id and is_admin:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Você não tem permissão para acessar esta página.")
            return redirect('home')
    return wrapper

def admin_required_for_delete(view_func):
    def wrapper(request, *args, **kwargs):
        # Checa se é um usuário do sistema ou colaborador logado
        is_admin = request.session.get('is_admin', False)  # para usuariosSistema
        usuario_id = request.session.get('usuario_id')
        
        if usuario_id and is_admin:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Você não tem permissão para deletar equipamentos.")
            return redirect('equipamento_list')
    return wrapper

def block_admin_access(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        is_admin = request.session.get('is_admin', False)
        usuario_id = request.session.get('usuario_id')
        
        if usuario_id and is_admin:
            messages.error(request, "Administradores não têm acesso a esta funcionalidade.")
            return redirect('emprestimo_list')
        return view_func(request, *args, **kwargs)
    return wrapper
