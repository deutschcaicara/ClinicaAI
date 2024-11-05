from django.db import models
from apps.prontuarios.models import Prontuario
from apps.profissionais.models import ProfissionalSaude

class Atendimento(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='atendimentos')
    profissional = models.ForeignKey(ProfissionalSaude, on_delete=models.SET_NULL, null=True, related_name='atendimentos')
    data_atendimento = models.DateTimeField()
    tipo_atendimento = models.CharField(max_length=100, choices=[
        ('consulta', 'Consulta'),
        ('emergencia', 'Emergência'),
        ('retorno', 'Retorno'),
    ])
    descricao = models.TextField()
    receita = models.TextField(blank=True)

    def __str__(self):
        return f"Atendimento em {self.data_atendimento.strftime('%d/%m/%Y')} por {self.profissional}"
