from django.db import models


class Recursos_humanosModel(models.Model):
    nome = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
class PagamentoFuncionario(models.Model):
    funcionario = models.CharField(max_length=255, verbose_name="Funcionário")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Pagamento")
    data_pagamento = models.DateField(verbose_name="Data do Pagamento")

    class Meta:
        verbose_name = "Pagamento de Funcionário"
        verbose_name_plural = "Pagamentos de Funcionários"
