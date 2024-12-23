# Módulo Agendamentos - Serializers (serializers.py)

from rest_framework import serializers
from django.utils import timezone
from .models import Agendamento
import uuid


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = "__all__"

    def validate(self, data):
        # Validação para garantir que a data e horário do agendamento sejam
        # futuros
        if data["data_agendamento"] < timezone.now().date():
            raise serializers.ValidationError("A data do agendamento deve ser futura.")
        if (
            data["data_agendamento"] == timezone.now().date()
            and data["horario_inicio"] <= timezone.now().time()
        ):
            raise serializers.ValidationError("O horário de início deve ser no futuro.")

        # Validação para garantir que o horário de fim seja posterior ao
        # horário de início
        if data["horario_fim"] <= data["horario_inicio"]:
            raise serializers.ValidationError(
                "O horário de fim deve ser posterior ao horário de início."
            )

        # Validação para garantir que não haja sobreposição de agendamentos
        # para o mesmo profissional
        agendamentos_existentes = Agendamento.objects.filter(
            profissional=data["profissional"],
            data_agendamento=data["data_agendamento"],
            horario_inicio__lt=data["horario_fim"],
            horario_fim__gt=data["horario_inicio"],
        ).exclude(uuid=data.get("uuid"))
        if agendamentos_existentes.exists():
            raise serializers.ValidationError(
                "O horário do agendamento conflita com outro agendamento existente para este profissional."
            )

        # Validação para garantir que não haja sobreposição de agendamentos
        # para o mesmo paciente
        agendamentos_paciente = Agendamento.objects.filter(
            paciente=data["paciente"],
            data_agendamento=data["data_agendamento"],
            horario_inicio__lt=data["horario_fim"],
            horario_fim__gt=data["horario_inicio"],
        ).exclude(uuid=data.get("uuid"))
        if agendamentos_paciente.exists():
            raise serializers.ValidationError(
                "O paciente já possui um agendamento no mesmo horário."
            )

        # Validação para garantir que o status financeiro esteja correto se o
        # agendamento for concluído
        if data["status"] == "Concluído" and data["status_financeiro"] != "Pago":
            raise serializers.ValidationError(
                "Agendamentos concluídos devem ter o status financeiro como 'Pago'."
            )

        # Validação para garantir que o motivo do cancelamento esteja
        # preenchido se o agendamento for cancelado
        if data["status"] == "Cancelado" and not data.get("motivo_cancelamento"):
            raise serializers.ValidationError(
                "O motivo do cancelamento deve ser informado quando o agendamento for cancelado."
            )

        # Validação para garantir que o canal preferencial de notificação seja
        # consistente com as preferências do paciente
        if data["canal_preferencial"] not in ["WhatsApp", "SMS", "Email"]:
            raise serializers.ValidationError(
                "Canal preferencial de notificação inválido."
            )

        # Validação para garantir a disponibilidade dos equipamentos e sala de
        # atendimento
        if data.get("equipamentos_necessarios") or data.get("sala_atendimento"):
            conflitos = Agendamento.objects.filter(
                data_agendamento=data["data_agendamento"],
                horario_inicio__lt=data["horario_fim"],
                horario_fim__gt=data["horario_inicio"],
                sala_atendimento=data.get("sala_atendimento"),
            ).exclude(uuid=data.get("uuid"))
            if conflitos.exists():
                raise serializers.ValidationError(
                    "A sala de atendimento ou equipamentos necessários já estão reservados para outro agendamento no mesmo horário."
                )

        # Validação para garantir que o profissional não esteja de férias ou
        # ausente na data de agendamento
        if (
            hasattr(data["profissional"], "ferias")
            and data["profissional"]
            .ferias.filter(
                inicio__lte=data["data_agendamento"], fim__gte=data["data_agendamento"]
            )
            .exists()
        ):
            raise serializers.ValidationError(
                "O profissional está de férias ou ausente na data selecionada."
            )

        # Validação para limitar o número de agendamentos do mesmo paciente no
        # mesmo dia
        limite_agendamentos_paciente = Agendamento.objects.filter(
            paciente=data["paciente"], data_agendamento=data["data_agendamento"]
        ).count()
        if limite_agendamentos_paciente >= 3:
            raise serializers.ValidationError(
                "O paciente já possui muitos agendamentos para o mesmo dia."
            )

        # Validação de pré-check-in
        if data.get("pre_checkin_realizado") and not data.get(
            "confirmado_pelo_paciente"
        ):
            raise serializers.ValidationError(
                "O pré-check-in não pode ser realizado sem a confirmação do paciente."
            )

        # Validação para garantir que o agendamento não ocorra em feriados ou
        # dias bloqueados
        if (
            hasattr(data["profissional"], "dias_bloqueados")
            and data["profissional"]
            .dias_bloqueados.filter(data=data["data_agendamento"])
            .exists()
        ):
            raise serializers.ValidationError(
                "O agendamento não pode ser feito em um feriado ou dia bloqueado para este profissional."
            )

        # Validação para garantir que o status seja consistente com a
        # confirmação do paciente
        if data["status"] == "Concluído" and not data.get("confirmado_pelo_paciente"):
            raise serializers.ValidationError(
                "O agendamento não pode ser concluído sem a confirmação do paciente."
            )

        return data
