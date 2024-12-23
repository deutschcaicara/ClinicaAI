# Módulo Exames - Models (models.py)

from django.db import models
from django.utils import timezone
import uuid
from apps.pacientes.models import Paciente
from apps.profissionais.models import Profissional
from apps.documentos.models import DocumentosModel


class Exame(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="exames"
    )
    profissional_solicitante = models.ForeignKey(
    Profissional,
    on_delete=models.SET_NULL,
    null=True,
    related_name="exames_solicitados_exame",  # Alterar para um nome único
    verbose_name="Profissional Solicitante",
)

    tipo_exame = models.CharField(max_length=100, verbose_name="Tipo de Exame")
    data_solicitacao = models.DateField(
        default=timezone.now, verbose_name="Data de Solicitação"
    )
    data_realizacao = models.DateField(
        blank=True, null=True, verbose_name="Data de Realização"
    )
    resultados = models.TextField(
        verbose_name="Resultados do Exame", blank=True, null=True
    )
    documento_resultado = models.ForeignKey(
        DocumentosModel,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="exames_resultados",
        verbose_name="Documento do Resultado",
    )
    observacoes = models.TextField(verbose_name="Observações", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Solicitado", "Solicitado"),
            ("Realizado", "Realizado"),
            ("Cancelado", "Cancelado"),
        ],
        default="Solicitado",
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-data_solicitacao"]
        verbose_name = "Exame"
        verbose_name_plural = "Exames"

    def __str__(self):
        return f"Exame {self.tipo_exame} de {self.paciente.nome_completo}"

    def is_realizado(self):
        return self.status == "Realizado"
