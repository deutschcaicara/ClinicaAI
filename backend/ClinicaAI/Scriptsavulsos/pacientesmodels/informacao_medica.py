from django.db import models
from .paciente import Paciente

class InformacaoMedica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='informacoes_medicas')
    historico_medico = models.TextField(help_text="Histórico médico detalhado do paciente.")
    alergias = models.TextField(null=True, blank=True, help_text="Alergias que o paciente possui.")
    medicamentos_em_uso = models.TextField(null=True, blank=True, help_text="Medicamentos atualmente em uso pelo paciente.")
    doencas_preexistentes = models.TextField(null=True, blank=True, help_text="Doenças preexistentes do paciente.")
    tipo_dependencia = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de dependência, como álcool, drogas sintéticas.")
    comorbidades_psiquiatricas = models.TextField(null=True, blank=True, help_text="Comorbidades psiquiátricas do paciente.")

    class Meta:
        verbose_name = "Informação Médica"
        verbose_name_plural = "Informações Médicas"

    def __str__(self):
        return f"Informações médicas de {self.paciente.nome}"
