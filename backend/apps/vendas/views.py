from rest_framework import viewsets
from .models import VendasModel
from .serializers import VendasSerializer

class VendasViewSet(viewsets.ModelViewSet):
    queryset = VendasModel.objects.all()
    serializer_class = VendasSerializer
