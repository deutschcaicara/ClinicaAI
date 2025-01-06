from rest_framework import viewsets
from .models import IndicacoesModel
from .serializers import IndicacoesSerializer


class IndicacoesViewSet(viewsets.ModelViewSet):
    queryset = IndicacoesModel.objects.all()
    serializer_class = IndicacoesSerializer
