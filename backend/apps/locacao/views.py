from rest_framework import viewsets
from .models import LocacaoModel
from .serializers import LocacaoSerializer

class LocacaoViewSet(viewsets.ModelViewSet):
    queryset = LocacaoModel.objects.all()
    serializer_class = LocacaoSerializer
