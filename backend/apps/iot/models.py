from django.db import models


class DispositivoIoT(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do Dispositivo")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    status = models.CharField(
        max_length=100,
        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
        default="ativo",
    )
    data_registro = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Registro"
    )
    ultima_comunicacao = models.DateTimeField(
        blank=True, null=True, verbose_name="Última Comunicação"
    )

    class Meta:
        verbose_name = "Dispositivo IoT"
        verbose_name_plural = "Dispositivos IoT"

    def __str__(self):
        return self.nome
