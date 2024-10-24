from rest_framework import viewsets
from .models import AvaliacoesModel
from .serializers import AvaliacoesSerializer

class AvaliacoesViewSet(viewsets.ModelViewSet):
    queryset = AvaliacoesModel.objects.all()
    serializer_class = AvaliacoesSerializer
