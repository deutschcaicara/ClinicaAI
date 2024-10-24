from rest_framework import viewsets
from .models import PlmModel
from .serializers import PlmSerializer

class PlmViewSet(viewsets.ModelViewSet):
    queryset = PlmModel.objects.all()
    serializer_class = PlmSerializer
