from rest_framework import viewsets
from .models import FolgasModel
from .serializers import FolgasSerializer


class FolgasViewSet(viewsets.ModelViewSet):
    queryset = FolgasModel.objects.all()
    serializer_class = FolgasSerializer
