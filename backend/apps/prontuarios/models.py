
from django.db import models
from apps.pacientes.models import Paciente

class Prontuario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='prontuarios')
    data_registro = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    medico_responsavel = models.CharField(max_length=100)

    def __str__(self):
        return f"Prontuário de {self.paciente.nome_completo} - {self.data_registro.strftime('%d/%m/%Y')}"
