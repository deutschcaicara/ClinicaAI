from rest_framework import viewsets
from .models import CompromissosModel
from .serializers import CompromissosSerializer


class CompromissosViewSet(viewsets.ModelViewSet):
    queryset = CompromissosModel.objects.all()
    serializer_class = CompromissosSerializer
