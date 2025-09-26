from django.db import models
from django.utils import timezone
from app_EPINav.models.colaborador import Colaborador
from app_EPINav.models.equipamento import Equipamento

class Emprestimo(models.Model):
    colaborador = models.ForeignKey(
        Colaborador, on_delete=models.CASCADE, related_name="emprestimos"
    )
    equipamento = models.ForeignKey(
        Equipamento, on_delete=models.CASCADE, related_name="emprestimos"
    )
    data_entrega = models.DateTimeField(default=timezone.now)
    data_prevista_devolucao = models.DateTimeField()
    data_devolucao = models.DateTimeField(blank=True, null=True)
    observacao_devolucao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.equipamento.nome} - {self.colaborador.nome}"

    def save(self, *args, **kwargs):
        """Atualiza o estado do equipamento conforme o empréstimo."""
        if not self.pk:  # criando novo empréstimo
            self.equipamento.estado = "emprestado"
            self.equipamento.save(update_fields=["estado"])
        elif self.data_devolucao:  # se foi devolvido
            self.equipamento.estado = "devolvido"
            self.equipamento.save(update_fields=["estado"])

        super().save(*args, **kwargs)
