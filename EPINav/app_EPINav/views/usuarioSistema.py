from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app_EPINav.models.usuario import UsuarioSistema
from app_EPINav.forms.usuarioSistema import UsuarioSistemaForm
from app_EPINav.views.decorators import login_required_custom, admin_required

# Login
@login_required_custom
@admin_required
def login_view(request):
    if request.method == "POST":
        nome_usuario = request.POST.get("nome_usuario")
        senha = request.POST.get("senha")
        try:
            user = UsuarioSistema.objects.get(nome_usuario=nome_usuario)
            if user.check_password(senha):
                request.session['usuario_id'] = user.id
                request.session['tipo_usuario'] = 'usuarioSistema'
                request.session['is_admin'] = user.is_admin
                return redirect("home")
            else:
                messages.error(request, "Senha incorreta")
        except UsuarioSistema.DoesNotExist:
            messages.error(request, "Usuário não encontrado")
    return render(request, "app_EPINav/pages/login.html")

# Logout
@login_required_custom
@admin_required
def logout_view(request):
    request.session.flush()
    return redirect("login")


# Listar usuários
@login_required_custom
@admin_required
def listar_usuarios(request):
    usuarios = UsuarioSistema.objects.all()
    return render(request, "app_EPINav/pages/usuarioSistema/usuario_list.html", {"usuarios": usuarios})


# Criar usuário
@login_required_custom
@admin_required
def criar_usuario(request):
    if request.method == "POST":
        form = UsuarioSistemaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário criado com sucesso!")
            return redirect("usuario_list")
    else:
        form = UsuarioSistemaForm()
    return render(request, "app_EPINav/pages/usuarioSistema/usuario_form.html", {"form": form})


# Editar usuário
@login_required_custom
@admin_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(UsuarioSistema, pk=pk)
    if request.method == "POST":
        form = UsuarioSistemaForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect("usuario_list")
    else:
        form = UsuarioSistemaForm(instance=usuario)
    return render(request, "app_EPINav/pages/usuarioSistema/usuario_form.html", {"form": form, "object": usuario})


# Deletar usuário
@login_required_custom
@admin_required
def deletar_usuario(request, pk):
    usuario = get_object_or_404(UsuarioSistema, pk=pk)
    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuário deletado com sucesso!")
        return redirect("usuario_list")
    return redirect("usuario_list")
