# Módulo Profissionais - Views (views.py)

from rest_framework import viewsets, status
from .models import Especialidade, Profissional, Disponibilidade, RegistroHorasTrabalhadas
from .serializers import EspecialidadeSerializer, ProfissionalSerializer, DisponibilidadeSerializer, RegistroHorasTrabalhadasSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

# Custom Permissions
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        return request.user and request.user.is_staff

class IsProfissionalOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.usuario == request.user or request.user.is_staff

# Views
class EspecialidadeViewSet(viewsets.ModelViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class DisponibilidadeViewSet(viewsets.ModelViewSet):
    queryset = Disponibilidade.objects.all()
    serializer_class = DisponibilidadeSerializer
    permission_classes = [IsAuthenticated, IsProfissionalOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Validar se a disponibilidade é para uma data futura
        data = request.data.copy()
        dia = data.get('dia')
        if dia:
            dia = timezone.datetime.strptime(dia, '%Y-%m-%d').date()
            if dia < timezone.now().date():
                return Response({"detail": "A disponibilidade deve ser para uma data futura."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

class RegistroHorasTrabalhadasViewSet(viewsets.ModelViewSet):
    queryset = RegistroHorasTrabalhadas.objects.all()
    serializer_class = RegistroHorasTrabalhadasSerializer
    permission_classes = [IsAuthenticated, IsProfissionalOrReadOnly]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def minhas_horas(self, request):
        # Retornar as horas trabalhadas do profissional autenticado
        if hasattr(request.user, 'profissional'):
            profissional = request.user.profissional
            queryset = RegistroHorasTrabalhadas.objects.filter(profissional=profissional)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"detail": "Usuário não é um profissional."}, status=status.HTTP_400_BAD_REQUEST)
