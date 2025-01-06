from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.profissionais.models import Profissional

from apps.pacientes.models import Paciente

import uuid


class Agendamento(models.Model):
    # Identificador Único Global
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    paciente = models.ForeignKey(
    'pacientes.Paciente', on_delete=models.CASCADE, related_name='agendamentos'
)




    profissional = models.ForeignKey(
        Profissional, on_delete=models.CASCADE, related_name="agendamentos_profissional"
    )

    # Dados do Agendamento
    data_agendamento = models.DateField(verbose_name=_("Data do Agendamento"))
    horario_inicio = models.TimeField(verbose_name=_("Horário de Início"))
    horario_fim = models.TimeField(verbose_name=_("Horário de Fim"))
    tipo_consulta = models.CharField(
        max_length=50,
        choices=[
            ("Consulta Inicial", "Consulta Inicial"),
            ("Retorno", "Retorno"),
            ("Exame", "Exame"),
            ("Teleconsulta", "Teleconsulta"),
        ],
        default="Consulta Inicial",
        verbose_name=_("Tipo de Consulta"),
    )
    local_atendimento = models.CharField(
        max_length=50,
        choices=[
            ("Presencial", "Presencial"),
            ("Telemedicina", "Telemedicina"),
            ("Visita Domiciliar", "Visita Domiciliar"),
        ],
        default="Presencial",
        verbose_name=_("Local do Atendimento"),
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("Agendado", "Agendado"),
            ("Cancelado", "Cancelado"),
            ("Concluído", "Concluído"),
        ],
        default="Agendado",
        verbose_name=_("Status do Agendamento"),
    )
    motivo_cancelamento = models.TextField(
        blank=True, null=True, verbose_name=_("Motivo do Cancelamento")
    )
    confirmado_pelo_paciente = models.BooleanField(
        default=False, verbose_name=_("Confirmado pelo Paciente")
    )
    observacoes = models.TextField(blank=True, verbose_name=_("Observações"))
    sintomas_iniciais = models.TextField(
        blank=True, verbose_name=_("Sintomas Iniciais")
    )
    tipo_atendimento = models.CharField(
        max_length=20,
        choices=[("Emergencial", "Emergencial"), ("Rotina", "Rotina")],
        default="Rotina",
        verbose_name=_("Tipo de Atendimento"),
    )
    motivo_consulta = models.CharField(
        max_length=255, blank=True, verbose_name=_("Motivo da Consulta")
    )

    # Dados Financeiros
    meio_pagamento = models.CharField(
        max_length=50,
        choices=[
            ("Cartão de Crédito", "Cartão de Crédito"),
            ("Convênio", "Convênio"),
            ("Dinheiro", "Dinheiro"),
            ("PIX", "PIX"),
        ],
        blank=True,
        verbose_name=_("Meio de Pagamento"),
    )
    status_financeiro = models.CharField(
        max_length=20,
        choices=[("Pago", "Pago"), ("Pendente", "Pendente")],
        default="Pendente",
        verbose_name=_("Status Financeiro"),
    )

    # Notificações e Lembretes
    canal_preferencial = models.CharField(
        max_length=20,
        choices=[("WhatsApp", "WhatsApp"), ("SMS", "SMS"), ("Email", "Email")],
        default="WhatsApp",
        verbose_name=_("Canal Preferencial de Notificação"),
    )
    lembrete_enviado_em = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Lembrete Enviado em")
    )
    status_notificacao = models.CharField(
        max_length=20,
        choices=[("Enviado", "Enviado"), ("Lido", "Lido"), ("Pendente", "Pendente")],
        default="Pendente",
        verbose_name=_("Status da Notificação"),
    )

    # Automação e Integração IoT
    equipamentos_necessarios = models.CharField(
        max_length=255, blank=True, verbose_name=_("Equipamentos Necessários")
    )
    sala_atendimento = models.CharField(
        max_length=50, blank=True, verbose_name=_("Sala de Atendimento")
    )
    dispositivo_iot = models.CharField(
        max_length=100, blank=True, verbose_name=_("Dispositivo IoT Necessário")
    )

    # Dados para IA e Machine Learning
    probabilidade_cancelamento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Probabilidade de Cancelamento (%)"),
    )
    tempo_espera_estimado = models.DurationField(
        blank=True, null=True, verbose_name=_("Tempo de Espera Estimado")
    )
    preferencias_paciente = models.CharField(
        max_length=255, blank=True, verbose_name=_("Preferências do Paciente")
    )
    confirmar_atendimento_automatico = models.BooleanField(
        default=False, verbose_name=_("Confirmar Atendimento Automaticamente")
    )

    # Histórico de Modificações
    log_modificacoes = models.TextField(
        blank=True, verbose_name=_("Histórico de Modificações")
    )
    historico_cancelamentos = models.TextField(
        blank=True, verbose_name=_("Histórico de Cancelamentos")
    )

    # Pré-Check-in
    pre_checkin_realizado = models.BooleanField(
        default=False, verbose_name=_("Pré-Check-in Realizado")
    )

    # Dados de Controle
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Agendamento")
        verbose_name_plural = _("Agendamentos")
        app_label = "agendamentos"
        unique_together = (("profissional", "data_agendamento", "horario_inicio"),)

    def __str__(self):
        return f"Agendamento de {self.paciente.nome_completo} com {self.profissional.nome_completo} em {self.data_agendamento} às {self.horario_inicio}"
