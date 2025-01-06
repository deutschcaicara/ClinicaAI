# Incremento 3: Melhorias nas Visualizações (views.py)

from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Paciente
from .serializers import PacienteSerializer
import logging

logger = logging.getLogger(__name__)

class PacientePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
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
        if self.action in ["list", "retrieve", "create", "update", "destroy"]:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        logger.debug("Listando pacientes")
        response = super().list(request, *args, **kwargs)
        logger.debug(f"Response data: {response.data}")
        return response

