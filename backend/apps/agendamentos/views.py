# Módulo Agendamentos - Views (views.py)

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Agendamento
from .serializers import AgendamentoSerializer
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import logging
import threading
import uuid

logger = logging.getLogger(__name__)


class AgendamentoViewSet(viewsets.ModelViewSet):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna os agendamentos futuros do usuário autenticado (paciente ou
        # profissional)
        user = self.request.user
        if hasattr(user, 'paciente'):
            return Agendamento.objects.filter(
    paciente=user.paciente,
     data_agendamento__gte=timezone.now().date())
        elif hasattr(user, 'profissional'):
            return Agendamento.objects.filter(
    profissional=user.profissional,
     data_agendamento__gte=timezone.now().date())
        return Agendamento.objects.none()

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def confirmar(self, request, pk=None):
        # Ação para confirmar o agendamento pelo paciente
        agendamento = self.get_object()
        if hasattr(
    request.user,
     'paciente') and agendamento.paciente != request.user.paciente:
            return Response(
    {
        'detail': 'Você não tem permissão para confirmar este agendamento.'},
         status=status.HTTP_403_FORBIDDEN)

        if agendamento.confirmado_pelo_paciente:
            return Response({'detail': 'Agendamento já foi confirmado.'},
                            status=status.HTTP_400_BAD_REQUEST)

        agendamento.confirmado_pelo_paciente = True
        agendamento.save()

       

    @ action(detail=True, methods=['post'],
             permission_classes=[IsAuthenticated])
    def cancelar(self, request, pk=None):
        # Ação para cancelar um agendamento
        agendamento= self.get_object()
        motivo= request.data.get('motivo_cancelamento')
        if not motivo:
            return Response({'detail': 'Motivo do cancelamento deve ser informado.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Verificar permissões de cancelamento
        if hasattr(
    request.user,
     'paciente') and agendamento.paciente != request.user.paciente:
            return Response(
    {
        'detail': 'Você não tem permissão para cancelar este agendamento.'},
         status = status.HTTP_403_FORBIDDEN)
        if hasattr(
    request.user,
     'profissional') and agendamento.profissional != request.user.profissional:
            return Response(
    {
        'detail': 'Você não tem permissão para cancelar este agendamento.'},
         status = status.HTTP_403_FORBIDDEN)

        agendamento.status= 'Cancelado'
        agendamento.motivo_cancelamento= motivo
        agendamento.save()

       

    @ action(detail=True, methods=['post'],
             permission_classes=[IsAuthenticated])
    def reagendar(self, request, pk=None):
        # Ação para reagendar um agendamento
        agendamento= self.get_object()
        nova_data= request.data.get('data_agendamento')
        novo_horario_inicio= request.data.get('horario_inicio')
        novo_horario_fim= request.data.get('horario_fim')

        if not nova_data or not novo_horario_inicio or not novo_horario_fim:
            return Response({'detail': 'Dados de reagendamento incompletos.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validação para garantir que a nova data e horário sejam futuros
        if nova_data < timezone.now().date() or (nova_data == timezone.now().date()
                                    and novo_horario_inicio <= timezone.now().time()):
            return Response({'detail': 'A nova data e horário devem ser no futuro.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validação para garantir que a capacidade da sala não seja excedida
        # (Exemplo para IoT)
        if agendamento.sala_atendimento:
            capacidade_sala= agendamento.sala_atendimento.capacidade  # Supondo que o modelo de sala tenha um campo 'capacidade'
            ocupacao_atual= Agendamento.objects.filter(
                data_agendamento=nova_data,
                horario_inicio__lt=novo_horario_fim,
                horario_fim__gt=novo_horario_inicio,
                sala_atendimento=agendamento.sala_atendimento
            ).count()
            if ocupacao_atual >= capacidade_sala:
                return Response(
    {
        'detail': 'A capacidade da sala de atendimento foi excedida.'},
         status=status.HTTP_400_BAD_REQUEST)

        # Atualizar o agendamento com a nova data e horário
        agendamento.data_agendamento= nova_data
        agendamento.horario_inicio= novo_horario_inicio
        agendamento.horario_fim= novo_horario_fim
        agendamento.status= 'Agendado'
        agendamento.motivo_cancelamento= ''  # Limpar motivo de cancelamento, se houver
        agendamento.save()

     

    @ action(detail=False, methods=['get'],
             permission_classes=[IsAuthenticated])
    def meus_agendamentos(self, request):
        # Retorna os agendamentos do paciente ou profissional autenticado
        if hasattr(request.user, 'paciente'):
            agendamentos= Agendamento.objects.filter(paciente=request.user.paciente)
        elif hasattr(request.user, 'profissional'):
            agendamentos= Agendamento.objects.filter(profissional=request.user.profissional)
        else:
            return Response(
    {
        'detail': 'Você não tem permissão para visualizar agendamentos.'},
         status=status.HTTP_403_FORBIDDEN)

        serializer= self.get_serializer(agendamentos, many=True)
        return Response(serializer.data)
