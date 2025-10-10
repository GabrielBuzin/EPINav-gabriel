import pytest
from django.urls import reverse

from app_EPINav.models import Colaborador
from app_EPINav.models.usuario import UsuarioSistema

@pytest.mark.django_db
def handle(self, *args, **options):
    # Usuário admin
    admin_user, created = UsuarioSistema.objects.get_or_create(
        nome_usuario="admin",
        senha="",
        is_admin=True,
    )
    if created:
        UsuarioSistema.set_password(admin_user, "1234")
        UsuarioSistema.save(admin_user)
        self.stdout.write("UsuárioSistema admin criado (admin/1234)")
    else:
        self.stdout.write("UsuárioSistema admin já existe")

    # Colaborador padrão
    colaborador, created = Colaborador.objects.get_or_create(
        nome_usuario="colaborador1",
        defaults={
            "nome": "Colaborador 1",
            "cargo": "Funcionário",
            "status": "Ativo",
            "senha": "",
        }
    )
    if created:
        colaborador.set_password("1234")
        colaborador.save()
        self.stdout.write("Colaborador padrão criado (colaborador1/1234)")
    else:
        self.stdout.write("Colaborador padrão já existe")

def test_rota_retorna_home():
    url = reverse('home')
    assert url == '/'  # Verifica se a URL da rota 'home' é a raiz '/'
    
@pytest.mark.django_db
def test_rota_home_status_200(client):
    client.login(nome_usuario='admin', senha='1234')  # Faz login como admin
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200  # Verifica se a resposta da rota 'home' é 200 (OK)