from rest_framework import viewsets
from .models import Criador_sitesModel
from .serializers import Criador_sitesSerializer


class Criador_sitesViewSet(viewsets.ModelViewSet):
    queryset = Criador_sitesModel.objects.all()
    serializer_class = Criador_sitesSerializer
