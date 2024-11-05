from django.db import models
from apps.prontuarios.models import Prontuario
from apps.profissionais.models import ProfissionalSaude

class Exame(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='exames')
    tipo_exame = models.CharField(max_length=100)
    data_solicitacao = models.DateTimeField()
    data_resultado = models.DateTimeField(blank=True, null=True)
    resultado = models.TextField(blank=True)
    profissional_solicitante = models.ForeignKey(ProfissionalSaude, on_delete=models.SET_NULL, null=True, related_name='exames_solicitados')

    def __str__(self):
        return f"Exame {self.tipo_exame} solicitado em {self.data_solicitacao.strftime('%d/%m/%Y')}"
