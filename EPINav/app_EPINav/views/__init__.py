from .colaborador import (
    ColaboradorListView,
    ColaboradorCreateView,
    ColaboradorUpdateView,
    ColaboradorDeleteView
)

from .home import home

from .usuarioSistema import (
    login_view, logout_view,
    listar_usuarios, criar_usuario,
    editar_usuario, deletar_usuario
)

from .auth import *

from .decorators import *

from .equipamento import *