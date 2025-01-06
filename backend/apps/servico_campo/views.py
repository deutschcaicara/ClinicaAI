from rest_framework import viewsets
from .models import Servico_campoModel
from .serializers import Servico_campoSerializer


class Servico_campoViewSet(viewsets.ModelViewSet):
    queryset = Servico_campoModel.objects.all()
    serializer_class = Servico_campoSerializer
