from rest_framework import viewsets
from .models import FrotaModel
from .serializers import FrotaSerializer


class FrotaViewSet(viewsets.ModelViewSet):
    queryset = FrotaModel.objects.all()
    serializer_class = FrotaSerializer
