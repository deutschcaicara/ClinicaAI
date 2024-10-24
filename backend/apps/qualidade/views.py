from rest_framework import viewsets
from .models import QualidadeModel
from .serializers import QualidadeSerializer

class QualidadeViewSet(viewsets.ModelViewSet):
    queryset = QualidadeModel.objects.all()
    serializer_class = QualidadeSerializer
