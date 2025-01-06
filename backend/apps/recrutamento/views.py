from rest_framework import viewsets
from .models import RecrutamentoModel
from .serializers import RecrutamentoSerializer


class RecrutamentoViewSet(viewsets.ModelViewSet):
    queryset = RecrutamentoModel.objects.all()
    serializer_class = RecrutamentoSerializer
