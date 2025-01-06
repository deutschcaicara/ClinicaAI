from rest_framework import viewsets
from .models import Planilhas_horasModel
from .serializers import Planilhas_horasSerializer


class Planilhas_horasViewSet(viewsets.ModelViewSet):
    queryset = Planilhas_horasModel.objects.all()
    serializer_class = Planilhas_horasSerializer
