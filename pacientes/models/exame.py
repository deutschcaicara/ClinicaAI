from django.db import models
from .paciente import Paciente

class Exame(models.Model):
    paciente = models.ForeignKey(Paciente, related_name='exames', on_delete=models.CASCADE)
    tipo_exame = models.CharField(max_length=255)
    data_realizacao = models.DateField()
    resultado = models.TextField()
    arquivo_digitalizado = models.FileField(upload_to='exames/', null=True, blank=True)

    class Meta:
        verbose_name = 'Exame'
        verbose_name_plural = 'Exames'

    def __str__(self):
        return f"{self.tipo_exame} - {self.paciente.nome}"
