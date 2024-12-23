# Incremento 3: Melhorias nas Visualizações (views.py)

from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Paciente
from .serializers import PacienteSerializer


class PacientePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PacientePagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["sexo", "estado_civil", "cidade", "estado"]
    search_fields = ["nome_completo", "cpf", "email"]
    ordering_fields = ["nome_completo", "data_nascimento", "created_at"]
    ordering = ["nome_completo"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
