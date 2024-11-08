from rest_framework import viewsets
from .models import InventarioModel
from .serializers import InventarioSerializer


class InventarioViewSet(viewsets.ModelViewSet):
    queryset = InventarioModel.objects.all()
    serializer_class = InventarioSerializer
