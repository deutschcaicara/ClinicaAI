from rest_framework import viewsets
from .models import ComprasModel
from .serializers import ComprasSerializer

class ComprasViewSet(viewsets.ModelViewSet):
    queryset = ComprasModel.objects.all()
    serializer_class = ComprasSerializer
