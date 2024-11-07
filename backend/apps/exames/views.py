# Módulo Exames - Views (views.py)

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Exame
from .serializers import ExameSerializer
from django.utils import timezone
from notifications.services import NotificationService  # Serviço de notificação simulado
import threading

class ExameViewSet(viewsets.ModelViewSet):
    queryset = Exame.objects.all()
    serializer_class = ExameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna os exames do paciente autenticado ou exames solicitados por um profissional autenticado
        user = self.request.user
        if hasattr(user, 'paciente'):
            return Exame.objects.filter(paciente=user.paciente)
        elif hasattr(user, 'profissional'):
            return Exame.objects.filter(profissional_solicitante=user.profissional)
        return Exame.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def registrar_resultado(self, request, pk=None):
        # Ação para registrar o resultado de um exame
        exame = self.get_object()
        if hasattr(request.user, 'profissional') and exame.profissional_solicitante != request.user.profissional:
            return Response({'detail': 'Você não tem permissão para registrar o resultado deste exame.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(exame, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Enviar notificação para o paciente sobre o resultado do exame
        threading.Thread(target=NotificationService.send_notification, args=(
            'Resultado de Exame Disponível',
            f'O resultado do exame {exame.tipo_exame} está disponível.',
            [exame.paciente.usuario.email]
        )).start()

        # Adicionar integração com Machine Learning para análise dos resultados
        self.analisar_resultados(exame)

        return Response({'detail': 'Resultado do exame registrado com sucesso.'}, status=status.HTTP_200_OK)

    def analisar_resultados(self, exame):
        # Integração com Machine Learning para analisar resultados de exames
        # Simulação de chamada para um serviço de IA que analisa os resultados do exame
        if exame.resultados:
            threading.Thread(target=self.enviar_para_analise_ml, args=(exame,)).start()

    def enviar_para_analise_ml(self, exame):
        # Simulação de envio dos resultados do exame para um serviço de Machine Learning
        # Aqui pode ser feita a integração com um serviço externo de análise de saúde
        print(f"Enviando resultados do exame {exame.tipo_exame} para análise de IA.")
        # Implementar a lógica real de integração aqui

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancelar_exame(self, request, pk=None):
        # Ação para cancelar um exame
        exame = self.get_object()
        if hasattr(request.user, 'profissional') and exame.profissional_solicitante != request.user.profissional:
            return Response({'detail': 'Você não tem permissão para cancelar este exame.'}, status=status.HTTP_403_FORBIDDEN)

        exame.status = 'Cancelado'
        exame.save()

        # Enviar notificação para o paciente sobre o cancelamento do exame
        threading.Thread(target=NotificationService.send_notification, args=(
            'Exame Cancelado',
            f'O exame {exame.tipo_exame} foi cancelado.',
            [exame.paciente.usuario.email]
        )).start()

        return Response({'detail': 'Exame cancelado com sucesso.'}, status=status.HTTP_200_OK)
