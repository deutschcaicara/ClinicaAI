
from django.db import models
from apps.pacientes.models import Paciente

class Agendamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='agendamentos')
    data_horario = models.DateTimeField()
    tipo_consulta = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[
        ('agendado', 'Agendado'),
        ('cancelado', 'Cancelado'),
        ('realizado', 'Realizado'),
    ])
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"Agendamento de {self.paciente.nome_completo} em {self.data_horario}"
