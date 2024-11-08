from rest_framework import viewsets
from .models import Redes_sociaisModel
from .serializers import Redes_sociaisSerializer


class Redes_sociaisViewSet(viewsets.ModelViewSet):
    queryset = Redes_sociaisModel.objects.all()
    serializer_class = Redes_sociaisSerializer
