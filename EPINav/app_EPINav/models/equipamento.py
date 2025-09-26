from django.db import models

class Equipamento(models.Model):
    ESTADOS = [
        ('emprestado', 'Emprestado'),
        ('em_uso', 'Em uso'),
        ('fornecido', 'Fornecido'),
        ('devolvido', 'Devolvido'),
        ('danificado', 'Danificado'),
        ('perdido', 'Perdido'),
    ]
    nome = models.CharField(max_length=150, unique=True)
    descricao = models.TextField(blank=True, null=True)
    fabricante = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='fornecido')
    quantidade = models.PositiveIntegerField(default=1)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.fabricante}"
