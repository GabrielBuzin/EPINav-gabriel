from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app_EPINav.views import (
    ColaboradorListView,
    ColaboradorCreateView,
    ColaboradorUpdateView,
    ColaboradorDeleteView,
    home
)

from app_EPINav.views.usuarioSistema import (
    listar_usuarios, criar_usuario,
    editar_usuario, deletar_usuario
)

from app_EPINav.views.auth import login_view, logout_view

from app_EPINav.views.equipamento import (
    EquipamentoListView, EquipamentoCreateView,
    EquipamentoUpdateView, EquipamentoDeleteView
)
 
from app_EPINav.views import emprestimo

from app_EPINav.views import relatorio

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),

    # Colaboradores
    path('colaboradores/', ColaboradorListView.as_view(), name='colaborador_list'),
    path('colaboradores/novo/', ColaboradorCreateView.as_view(), name='colaborador_create'),
    path('colaboradores/<int:pk>/editar/', ColaboradorUpdateView.as_view(), name='colaborador_update'),
    path('colaboradores/<int:pk>/deletar/', ColaboradorDeleteView.as_view(), name='colaborador_delete'),

    # Usuários
    path('usuarios/', listar_usuarios, name='usuario_list'),
    path('usuarios/novo/', criar_usuario, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', editar_usuario, name='usuario_edit'),
    path('usuarios/<int:pk>/deletar/', deletar_usuario, name='usuario_delete'),
    
    # Equipamentos
    path('equipamentos/', EquipamentoListView.as_view(), name='equipamento_list'),
    path('equipamentos/novo/', EquipamentoCreateView.as_view(), name='equipamento_create'),
    path('equipamentos/<int:pk>/editar/', EquipamentoUpdateView.as_view(), name='equipamento_update'),
    path('equipamentos/<int:pk>/excluir/', EquipamentoDeleteView.as_view(), name='equipamento_delete'),
    
    # Emprestimo
    path("emprestimos/", emprestimo.EmprestimoListView.as_view(), name="emprestimo_list"),
    path("emprestimos/novo/", emprestimo.EmprestimoCreateView.as_view(), name="emprestimo_create"),
    path("emprestimos/<int:pk>/editar/", emprestimo.EmprestimoUpdateView.as_view(), name="emprestimo_update"),
    
    # Relatórios
    path("relatorios/", relatorio.relatorios, name="relatorios"),
    path("relatorios/<int:pk>/editar/", relatorio.editar_relatorio, name="relatorio_edit"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)