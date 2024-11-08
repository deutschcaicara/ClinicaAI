from rest_framework import viewsets
from .models import ProjetoModel
from .serializers import ProjetoSerializer


class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = ProjetoModel.objects.all()
    serializer_class = ProjetoSerializer
