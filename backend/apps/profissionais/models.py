# Módulo Profissionais - Criação do Modelo (models.py)

from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings


class Especialidade(models.Model):
    nome = models.CharField(
        max_length=100, unique=True, verbose_name=_("Nome da Especialidade")
    )
    descricao = models.TextField(blank=True, verbose_name=_("Descrição"))

    class Meta:
        verbose_name = _("Especialidade")
        verbose_name_plural = _("Especialidades")
        app_label = "profissionais"

    def __str__(self):
        return self.nome


class Profissional(models.Model):
    # Identificador Único Global
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # Dados Pessoais
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profissional",
        verbose_name=_("Usuário"),
    )
    nome_completo = models.CharField(max_length=255, verbose_name=_("Nome Completo"))
    cpf = models.CharField(max_length=11, unique=True, verbose_name=_("CPF"))
    registro_conselho = models.CharField(
        max_length=50, unique=True, verbose_name=_("Registro no Conselho")
    )
    conselho = models.CharField(
        max_length=100, verbose_name=_("Conselho de Classe (CRM, CRO, etc.)")
    )
    especialidades = models.ManyToManyField(
        Especialidade, related_name="profissionais", verbose_name=_("Especialidades")
    )
    telefone = models.CharField(max_length=20, blank=True, verbose_name=_("Telefone"))
    email = models.EmailField(max_length=255, verbose_name=_("E-mail"))
    endereco = models.CharField(max_length=255, blank=True, verbose_name=_("Endereço"))
    tipo_contratacao = models.CharField(
        max_length=50,
        choices=[
            ("CLT", "CLT"),
            ("PJ", "Pessoa Jurídica"),
            ("Freelancer", "Freelancer"),
        ],
        verbose_name=_("Tipo de Contratação"),
    )
    documentos = models.FileField(
        upload_to="documentos_profissionais/", blank=True, verbose_name=_("Documentos")
    )

    # Dados Profissionais
    horario_atendimento_inicio = models.TimeField(
        verbose_name=_("Horário de Início do Atendimento")
    )
    horario_atendimento_fim = models.TimeField(
        verbose_name=_("Horário de Fim do Atendimento")
    )
    dias_atendimento = models.CharField(
        max_length=50, verbose_name=_("Dias da Semana para Atendimento")
    )

    class Meta:
        verbose_name = _("Profissional")
        verbose_name_plural = _("Profissionais")

    def __str__(self):
        return f"{self.nome_completo} ({self.registro_conselho})"


class Disponibilidade(models.Model):
    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.CASCADE,
        related_name="disponibilidades",
        verbose_name=_("Profissional"),
    )
    dia = models.DateField(verbose_name=_("Dia da Disponibilidade"))
    horario_inicio = models.TimeField(verbose_name=_("Horário de Início"))
    horario_fim = models.TimeField(verbose_name=_("Horário de Fim"))
    disponivel = models.BooleanField(default=True, verbose_name=_("Disponível"))

    class Meta:
        verbose_name = _("Disponibilidade")
        verbose_name_plural = _("Disponibilidades")
        unique_together = (("profissional", "dia", "horario_inicio", "horario_fim"),)

    def __str__(self):
        return f"Disponibilidade de {self.profissional.nome_completo} em {self.dia}"


class RegistroHorasTrabalhadas(models.Model):
    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.CASCADE,
        related_name="horas_trabalhadas",
        verbose_name=_("Profissional"),
    )
    dia = models.DateField(verbose_name=_("Dia"))
    horas_trabalhadas = models.DecimalField(
        max_digits=4, decimal_places=2, verbose_name=_("Horas Trabalhadas")
    )

    class Meta:
        verbose_name = _("Registro de Horas Trabalhadas")
        verbose_name_plural = _("Registros de Horas Trabalhadas")

    def __str__(self):
        return f"Horas trabalhadas por {self.profissional.nome_completo} em {self.dia}"
