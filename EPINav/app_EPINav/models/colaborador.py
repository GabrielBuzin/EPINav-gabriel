import os
import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError


def validar_imagem(foto):
    # limite 20MB
    max_size_mb = 20
    if foto.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"O tamanho máximo permitido é {max_size_mb} MB.")

    valid_exts = ['.png', '.jpeg', '.jpg', '.img']
    ext = os.path.splitext(foto.name)[1].lower()
    if ext not in valid_exts:
        raise ValidationError("Formato de imagem inválido. Use PNG, JPEG, JPG ou IMG.")

def colaborador_foto_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('colaboradores', filename)

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Ativo")
    data_admissao = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    nome_usuario = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=128)
    foto = models.ImageField(
        upload_to=colaborador_foto_path,
        blank=True,
        null=True,
        validators=[validar_imagem]
    )

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)
        self.save(update_fields=['senha'])

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)

    def save(self, *args, **kwargs):
        # remove a foto antiga se trocar
        try:
            old = Colaborador.objects.get(pk=self.pk)
            if old.foto and old.foto != self.foto:
                if default_storage.exists(old.foto.name):
                    default_storage.delete(old.foto.name)
        except Colaborador.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.foto and default_storage.exists(self.foto.name):
            default_storage.delete(self.foto.name)
        super().delete(*args, **kwargs)

    def __str__(self):

        return self.nome
