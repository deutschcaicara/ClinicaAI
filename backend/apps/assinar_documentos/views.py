from rest_framework import viewsets
from .models import Assinar_documentosModel
from .serializers import Assinar_documentosSerializer


class Assinar_documentosViewSet(viewsets.ModelViewSet):
    queryset = Assinar_documentosModel.objects.all()
    serializer_class = Assinar_documentosSerializer
