# Módulo Prontuários - Views (views.py)

from . import views
# Módulo Prontuários - Views (views.py)

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import (
    Prontuario,
    HistoricoMedicamentos,
    EvolucaoClinica,
    DadosVitais,
    HistoricoAcessosProntuario,
    ExameComplementar,
    Anamnese,
)
from .serializers import (
    ProntuarioSerializer,
    HistoricoMedicamentosSerializer,
    EvolucaoClinicaSerializer,
    DadosVitaisSerializer,
    HistoricoAcessosProntuarioSerializer,
    ExameComplementarSerializer,
    AnamneseSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, SAFE_METHODS

# Custom permission to restrict read/write access based on user roles

class AnamneseViewSet(viewsets.ModelViewSet):
    queryset = Anamnese.objects.all()
    serializer_class = AnamneseSerializer

    @action(detail=True, methods=['post'])
    def sugerir_cid(self, request, pk=None):
        anamnese = self.get_object()
        texto = anamnese.texto

        # Simular integração com IA (NLP para análise)
        sugestoes = [
            {"codigo": "J18.0", "descricao": "Pneumonia", "relevancia": 0.85},
            {"codigo": "J20.9", "descricao": "Bronquite aguda", "relevancia": 0.75},
        ]
        return Response({"anamnese": texto, "sugestoes_cid": sugestoes}, status=status.HTTP_200_OK)
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsDoctorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.groups.filter(name="Doctor").exists()
            or request.user.is_staff
        )


# Views


class ProntuarioViewSet(viewsets.ModelViewSet):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer
    permission_classes = [IsAuthenticated]  # Exigir autenticação

    def create(self, request, *args, **kwargs):
        # Filtra campos sensíveis antes de criar
        data = request.data.copy()
        sensitive_fields = ["created_by", "updated_by", "uuid"]
        for field in sensitive_fields:
            data.pop(field, None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        # Filtra campos sensíveis antes de atualizar
        data = request.data.copy()
        sensitive_fields = ["created_by", "updated_by", "uuid"]
        for field in sensitive_fields:
            data.pop(field, None)
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ProntuarioList(APIView):
    def get(self, request):
        prontuarios = Prontuario.objects.all()
        serializer = ProntuarioSerializer(prontuarios, many=True)
        return Response(serializer.data)


class HistoricoMedicamentosViewSet(viewsets.ModelViewSet):
    queryset = HistoricoMedicamentos.objects.all()
    serializer_class = HistoricoMedicamentosSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Filtra campos sensíveis antes de criar
        data = request.data.copy()
        sensitive_fields = ["prescrito_por"]
        for field in sensitive_fields:
            if not request.user.is_staff:
                data.pop(field, None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        # Filtra campos sensíveis antes de atualizar
        data = request.data.copy()
        sensitive_fields = ["prescrito_por"]
        for field in sensitive_fields:
            if not request.user.is_staff:
                data.pop(field, None)
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class EvolucaoClinicaViewSet(viewsets.ModelViewSet):
    queryset = EvolucaoClinica.objects.all()
    serializer_class = EvolucaoClinicaSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrReadOnly]

    def update(self, request, *args, **kwargs):
        # Limitar campos que podem ser editados por diferentes tipos de
        # usuários
        data = request.data.copy()
        restricted_fields = ["data_evolucao", "profissional_responsavel"]
        if not request.user.is_staff:
            for field in restricted_fields:
                data.pop(field, None)
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class DadosVitaisViewSet(viewsets.ModelViewSet):
    queryset = DadosVitais.objects.all()
    serializer_class = DadosVitaisSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Filtra campos sensíveis antes de criar
        data = request.data.copy()
        sensitive_fields = [
            "pressao_arterial",
            "frequencia_cardiaca",
            "temperatura",
            "saturacao_oxigenio",
            "glicemia",
            "colesterol_total",
            "triglicerides",
        ]
        if (
            not request.user.groups.filter(name="Doctor").exists()
            and not request.user.is_staff
        ):
            for field in sensitive_fields:
                data.pop(field, None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        # Filtra campos sensíveis antes de atualizar
        data = request.data.copy()
        sensitive_fields = [
            "pressao_arterial",
            "frequencia_cardiaca",
            "temperatura",
            "saturacao_oxigenio",
            "glicemia",
            "colesterol_total",
            "triglicerides",
        ]
        if (
            not request.user.groups.filter(name="Doctor").exists()
            and not request.user.is_staff
        ):
            for field in sensitive_fields:
                data.pop(field, None)
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class HistoricoAcessosProntuarioViewSet(viewsets.ModelViewSet):
    queryset = HistoricoAcessosProntuario.objects.all()
    serializer_class = HistoricoAcessosProntuarioSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Restringir campos sensíveis durante a listagem
        if not request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset()).defer(
                "usuario", "tipo_acesso"
            )
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ExameComplementarViewSet(viewsets.ModelViewSet):
    queryset = ExameComplementar.objects.all()
    serializer_class = ExameComplementarSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Filtra campos sensíveis antes de criar
        data = request.data.copy()
        sensitive_fields = ["resultado", "imagem_associada"]
        if (
            not request.user.groups.filter(name="Doctor").exists()
            and not request.user.is_staff
        ):
            for field in sensitive_fields:
                data.pop(field, None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        # Filtra campos sensíveis antes de atualizar
        data = request.data.copy()
        sensitive_fields = ["resultado", "imagem_associada"]
        if (
            not request.user.groups.filter(name="Doctor").exists()
            and not request.user.is_staff
        ):
            for field in sensitive_fields:
                data.pop(field, None)
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# URL Routing (urls.py)

router = DefaultRouter()
router.register(r"prontuarios", views.ProntuarioViewSet)
router.register(r"historico_medicamentos", views.HistoricoMedicamentosViewSet)
router.register(r"evolucoes_clinicas", views.EvolucaoClinicaViewSet)
router.register(r"dados_vitais", views.DadosVitaisViewSet)
router.register(r"historico_acessos", views.HistoricoAcessosProntuarioViewSet)
router.register(r"exames_complementares", views.ExameComplementarViewSet)
router.register(r'anamneses', AnamneseViewSet, basename='anamnese')

urlpatterns = [
    path("", include(router.urls)),
]
