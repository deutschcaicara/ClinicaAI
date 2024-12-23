from rest_framework import viewsets
from .models import Recursos_humanosModel
from .serializers import Recursos_humanosSerializer


class Recursos_humanosViewSet(viewsets.ModelViewSet):
    queryset = Recursos_humanosModel.objects.all()
    serializer_class = Recursos_humanosSerializer
