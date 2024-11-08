from django.db import models


class Transacao(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=50, choices=[("receita", "Receita"), ("despesa", "Despesa")]
    )

    def __str__(self):
        return f"{self.descricao} - {self.valor}"
