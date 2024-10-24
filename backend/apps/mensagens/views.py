from rest_framework import viewsets
from .models import MensagensModel
from .serializers import MensagensSerializer

class MensagensViewSet(viewsets.ModelViewSet):
    queryset = MensagensModel.objects.all()
    serializer_class = MensagensSerializer
