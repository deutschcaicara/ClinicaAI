# Módulo Atendimentos - Serializers (serializers.py)

from rest_framework import serializers
from django.utils import timezone
from .models import Atendimento
from agendamentos.models import Agendamento
from financeiro.models import Transacao
from documentos.models import DocumentoAssinado
from notifications.services import NotificationService  # Serviço de notificação simulado

class AtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        fields = '__all__'

    def validate(self, data):
        # Validação para garantir que a data e horário do atendimento sejam futuros, caso o atendimento ainda esteja pendente
        if data['status'] == 'Pendente' and (data['data_atendimento'] < timezone.now().date() or (data['data_atendimento'] == timezone.now().date() and data['horario_inicio'] <= timezone.now().time())):
            raise serializers.ValidationError("A data e o horário do atendimento pendente devem ser futuros.")

        # Garantir que a hora de fim do atendimento seja posterior à hora de início
        if data['horario_fim'] <= data['horario_inicio']:
            raise serializers.ValidationError("O horário de fim deve ser posterior ao horário de início.")

        # Validação para garantir que o agendamento associado não tenha sido concluído antes do atendimento
        agendamento = data.get('agendamento')
        if agendamento and agendamento.status == 'Concluído':
            raise serializers.ValidationError("O agendamento associado já foi concluído e não pode ser usado para um novo atendimento.")

        # Garantir que a assinatura do profissional e a autorização do paciente estejam presentes ao concluir o atendimento
        if data['status'] == 'Concluído':
            if not data.get('assinatura_profissional'):
                raise serializers.ValidationError("A assinatura do profissional é obrigatória para concluir o atendimento.")
            if not data.get('autorizacao_paciente'):
                raise serializers.ValidationError("A autorização do paciente é obrigatória para concluir o atendimento.")

        # Garantir que diagnóstico e feedback estejam presentes ao concluir o atendimento
        if data['status'] == 'Concluído':
            if not data.get('diagnostico'):
                raise serializers.ValidationError("O diagnóstico é obrigatório para concluir o atendimento.")
            if not data.get('feedback_paciente'):
                raise serializers.ValidationError("O feedback do paciente é obrigatório para concluir o atendimento.")

        return data

    def create(self, validated_data):
        # Lógica adicional ao criar um atendimento, como atualizar o status do agendamento relacionado
        agendamento = validated_data.get('agendamento')
        if agendamento:
            agendamento.status = 'Concluído'
            agendamento.save()

        # Enviar notificação para o paciente e profissional sobre a criação do atendimento
        NotificationService.send_notification(
            'Novo Atendimento Criado',
            f'Um novo atendimento foi agendado para {validated_data.get("data_atendimento")} com o profissional {validated_data.get("profissional").nome_completo}.',
            [validated_data.get('paciente').usuario.email, validated_data.get('profissional').usuario.email]
        )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Atualizar a transação financeira, se houver alteração no status do atendimento
        if 'status' in validated_data and validated_data['status'] == 'Concluído' and not instance.transacao_financeira:
            # Garantir que o valor do atendimento seja positivo
            valor = validated_data.get('valor', 0)
            if valor <= 0:
                raise serializers.ValidationError("O valor do atendimento deve ser positivo para criar uma transação financeira.")

            # Criar uma transação financeira relacionada
            transacao = Transacao.objects.create(
                paciente=instance.paciente,
                valor=valor,
                descricao=f'Pagamento pelo atendimento realizado em {instance.data_atendimento}',
                status='Pendente'
            )
            instance.transacao_financeira = transacao

        # Garantir que o status seja consistente com os campos obrigatórios
        if validated_data.get('status') == 'Concluído':
            if not instance.tratamento or not instance.prescricao:
                raise serializers.ValidationError("O atendimento não pode ser concluído sem um tratamento e uma prescrição adequados.")

        # Enviar notificação para o paciente e profissional sobre a conclusão do atendimento
        if validated_data.get('status') == 'Concluído':
            NotificationService.send_notification(
                'Atendimento Concluído',
                f'O atendimento de {instance.paciente.nome_completo} com o profissional {instance.profissional.nome_completo} foi concluído.',
                [instance.paciente.usuario.email, instance.profissional.usuario.email]
            )

        # Atualizar o status do agendamento para manter a consistência
        if instance.agendamento:
            instance.agendamento.status = 'Concluído'
            instance.agendamento.save()

        return super().update(instance, validated_data)
