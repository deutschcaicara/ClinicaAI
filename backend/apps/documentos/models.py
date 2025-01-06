from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentosModel(models.Model):
    nome = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Documento")
        verbose_name_plural = _("Documentos")
        app_label = "documentos"

    def __str__(self):
        return self.nome
