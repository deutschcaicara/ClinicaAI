from rest_framework import viewsets
from .models import LogSistema, Documento
from .serializers import LogSistemaSerializer, DocumentoSerializer
from rest_framework.permissions import IsAuthenticated

class LogSistemaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogSistema.objects.all()
    serializer_class = LogSistemaSerializer
    permission_classes = [IsAuthenticated]

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated]
