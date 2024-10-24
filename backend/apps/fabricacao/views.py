from rest_framework import viewsets
from .models import FabricacaoModel
from .serializers import FabricacaoSerializer

class FabricacaoViewSet(viewsets.ModelViewSet):
    queryset = FabricacaoModel.objects.all()
    serializer_class = FabricacaoSerializer
