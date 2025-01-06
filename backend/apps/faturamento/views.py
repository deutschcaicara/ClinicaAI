from rest_framework import viewsets
from .models import FaturamentoModel
from .serializers import FaturamentoSerializer


class FaturamentoViewSet(viewsets.ModelViewSet):
    queryset = FaturamentoModel.objects.all()
    serializer_class = FaturamentoSerializer
