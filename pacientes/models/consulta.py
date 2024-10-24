from django.db import models
from django.utils import timezone
from .paciente import Paciente

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, related_name='consultas', on_delete=models.CASCADE)
    data_consulta = models.DateTimeField(default=timezone.now)
    anamnese = models.TextField(null=True, blank=True)
    prescricoes = models.TextField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def __str__(self):
        return f"Consulta de {self.paciente.nome} em {self.data_consulta.strftime('%d/%m/%Y')}"
