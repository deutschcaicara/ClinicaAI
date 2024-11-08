# Módulo Atendimentos - Views (views.py)

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Atendimento
from .serializers import AtendimentoSerializer
from django.utils import timezone
import threading


class IsProfissional(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(
    request, view) and hasattr(
        request.user, 'profissional')


class AtendimentoViewSet(viewsets.ModelViewSet):
    queryset = Atendimento.objects.all()
    serializer_class = AtendimentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna os atendimentos do usuário autenticado (paciente ou
        # profissional)
        user = self.request.user
        if hasattr(user, 'paciente'):
            return Atendimento.objects.filter(paciente=user.paciente)
        elif hasattr(user, 'profissional'):
            return Atendimento.objects.filter(profissional=user.profissional)
        return Atendimento.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[IsProfissional])
    def concluir(self, request, pk=None):
        # Ação para concluir um atendimento
        atendimento = self.get_object()
        if atendimento.profissional != request.user.profissional:
            return Response(
    {
        'detail': 'Você não tem permissão para concluir este atendimento.'},
         status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(
    atendimento, data={
        'status': 'Concluído'}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        

        return Response(
            {'detail': 'Atendimento concluído com sucesso.'}, status=status.HTTP_200_OK)

    @ action(detail=False, methods=['get'],
             permission_classes=[IsAuthenticated])
    def meus_atendimentos(self, request):
        # Retorna os atendimentos do paciente ou profissional autenticado
        user= self.request.user
        if hasattr(user, 'paciente'):
            atendimentos= Atendimento.objects.filter(paciente=user.paciente)
        elif hasattr(user, 'profissional'):
            atendimentos= Atendimento.objects.filter(profissional=user.profissional)
        else:
            return Response(
    {
        'detail': 'Você não tem permissão para visualizar atendimentos.'},
         status = status.HTTP_403_FORBIDDEN)

        serializer= self.get_serializer(atendimentos, many=True)
        return Response(serializer.data)

    @ action(detail=True, methods=['post'],
             permission_classes=[IsProfissional])
    def cancelar(self, request, pk=None):
        # Ação para cancelar um atendimento
        atendimento= self.get_object()
        if atendimento.profissional != request.user.profissional:
            return Response(
    {
        'detail': 'Você não tem permissão para cancelar este atendimento.'},
         status = status.HTTP_403_FORBIDDEN)

        motivo= request.data.get('motivo_cancelamento')
        if not motivo:
            return Response({'detail': 'Motivo do cancelamento deve ser informado.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer= self.get_serializer(atendimento, data={'status': 'Cancelado'}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

       

    @ action(detail=True, methods=['post'],
             permission_classes=[IsProfissional])
    def reagendar(self, request, pk=None):
        # Ação para reagendar um atendimento
        atendimento= self.get_object()
        if atendimento.profissional != request.user.profissional:
            return Response(
    {
        'detail': 'Você não tem permissão para reagendar este atendimento.'},
         status=status.HTTP_403_FORBIDDEN)

        nova_data= request.data.get('data_atendimento')
        novo_horario_inicio= request.data.get('horario_inicio')
        novo_horario_fim= request.data.get('horario_fim')

        if not nova_data or not novo_horario_inicio or not novo_horario_fim:
            return Response({'detail': 'Dados de reagendamento incompletos.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer= self.get_serializer(atendimento, data={
            'data_atendimento': nova_data,
            'horario_inicio': novo_horario_inicio,
            'horario_fim': novo_horario_fim,
            'status': 'Pendente'
        }, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    #finalizzar o arquivo views.py
    
