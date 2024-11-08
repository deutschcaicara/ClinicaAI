from rest_framework import viewsets
from .models import ManutencaoModel
from .serializers import ManutencaoSerializer


class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = ManutencaoModel.objects.all()
    serializer_class = ManutencaoSerializer
