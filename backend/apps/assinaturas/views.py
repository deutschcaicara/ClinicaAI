# Módulo Assinaturas - Views (views.py)

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Documento, Assinatura
from .serializers import DocumentoSerializer, AssinaturaSerializer
from django.utils import timezone
import threading
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


def enviar_notificacao(titulo, mensagem, destinatarios):
    # Função de envio de notificação (placeholder)
    pass

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna os documentos do paciente ou profissional autenticado
        user = self.request.user
        if hasattr(user, 'paciente'):
            return Documento.objects.filter(paciente=user.paciente)
        elif hasattr(user, 'profissional'):
            return Documento.objects.filter(autor=user.profissional)
        return Documento.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def assinar(self, request, pk=None):
        # Ação para assinar um documento
        documento = self.get_object()
        if hasattr(request.user, 'profissional'):
            profissional = request.user.profissional

            # Verificar se o documento está expirado antes de permitir a assinatura
            if documento.is_expired():
                return Response(
                    {'detail': 'Não é possível assinar um documento expirado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            dados_assinatura = {
                'documento': documento.id,
                'assinante': profissional.id,
                'dupla_autenticacao': request.data.get('dupla_autenticacao', False),
                'biometria_hash': request.data.get('biometria_hash', None),
                'ip_assinatura': request.META.get('REMOTE_ADDR'),
                'localizacao_assinatura': request.data.get('localizacao_assinatura', None)
            }
            serializer = AssinaturaSerializer(data=dados_assinatura)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except ValidationError as e:
                logger.error(f"Erro ao validar assinatura: {e}")
                return Response({'detail': 'Erro ao validar assinatura.', 'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

            # Atualiza o status do documento para "Assinado" se necessário
            documento.status = 'Assinado'
            documento.save()

            # Enviar notificação para o paciente ou partes interessadas
            threading.Thread(target=enviar_notificacao, args=(
                'Documento Assinado',
                f'O documento "{documento.titulo}" foi assinado pelo profissional {profissional.nome_completo}.',
                [documento.paciente.usuario.email] if documento.paciente else []
            )).start()

            return Response({'detail': 'Documento assinado com sucesso.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)


class AssinaturaViewSet(viewsets.ModelViewSet):
    queryset = Assinatura.objects.all()
    serializer_class = AssinaturaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna as assinaturas do profissional autenticado
        user = self.request.user
        if hasattr(user, 'profissional'):
            return Assinatura.objects.filter(assinante=user.profissional)
        return Assinatura.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def validar_assinatura(self, request, pk=None):
        # Ação para validar a integridade da assinatura
        assinatura = self.get_object()
        if assinatura.validar_biometria(request.data.get('biometria_dados', '')):
            return Response({'detail': 'A assinatura é válida.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'A integridade da assinatura não foi confirmada.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancelar_assinatura(self, request, pk=None):
        # Ação para cancelar uma assinatura
        assinatura = self.get_object()
        if assinatura.assinante.usuario == request.user:
            assinatura.delete()
            assinatura.documento.status = 'Pendente'
            assinatura.documento.save()
            return Response({'detail': 'Assinatura cancelada com sucesso.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Você não tem permissão para cancelar esta assinatura.'}, status=status.HTTP_403_FORBIDDEN)
