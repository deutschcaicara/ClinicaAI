from rest_framework import viewsets
from .models import DocumentosModel
from .serializers import DocumentosSerializer


class DocumentosViewSet(viewsets.ModelViewSet):
    queryset = DocumentosModel.objects.all()
    serializer_class = DocumentosSerializer
