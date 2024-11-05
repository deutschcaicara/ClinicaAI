from django.db import models

class ProfissionalSaude(models.Model):
    nome_completo = models.CharField(max_length=255)
    especialidade = models.CharField(max_length=100)
    registro_profissional = models.CharField(max_length=50)
    contato = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.nome_completo} - {self.especialidade}"
