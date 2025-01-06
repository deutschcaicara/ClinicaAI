from rest_framework import viewsets
from .models import ElearningModel
from .serializers import ElearningSerializer


class ElearningViewSet(viewsets.ModelViewSet):
    queryset = ElearningModel.objects.all()
    serializer_class = ElearningSerializer
