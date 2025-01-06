from django.db import models

class Fornecedor(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do Fornecedor")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ["-criado_em"]

    def __str__(self):
        return self.nome
class PedidoFornecedor(models.Model):
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total")
    data_pedido = models.DateField(verbose_name="Data do Pedido")

    class Meta:
        verbose_name = "Pedido de Fornecedor"
        verbose_name_plural = "Pedidos de Fornecedores"
