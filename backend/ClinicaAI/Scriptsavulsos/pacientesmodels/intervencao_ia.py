# Criar o arquivo intervencao_ia.py em /mnt/dados/clinicaai/pacientes/models/

from django.db import models
from .paciente import Paciente

class IntervencaoIA(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='intervencoes_ia')
    descricao_intervencao = models.TextField(help_text="Descrição da intervenção sugerida pela IA.")
    tipo_intervencao = models.CharField(max_length=50, choices=[
        ('ajuste_medicamento', 'Ajuste de Medicamento'),
        ('mudanca_tratamento', 'Mudança de Tratamento'),
        ('triagem_prioritaria', 'Triagem Prioritária'),
        ('risco_alto', 'Avaliação de Risco Alto')
    ])
    data_intervencao = models.DateTimeField(auto_now_add=True)
    responsavel_aprovacao = models.CharField(max_length=255, null=True, blank=True, help_text="Profissional que aprovou a intervenção.")
    status = models.CharField(max_length=50, choices=[
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada')
    ], default='pendente')

    class Meta:
        verbose_name = "Intervenção de IA"
        verbose_name_plural = "Intervenções de IA"

    def __str__(self):
        return f"Intervenção IA - {self.paciente.nome} ({self.tipo_intervencao})"
