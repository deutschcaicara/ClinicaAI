from rest_framework import viewsets
from .models import DespesasModel
from .serializers import DespesasSerializer


class DespesasViewSet(viewsets.ModelViewSet):
    queryset = DespesasModel.objects.all()
    serializer_class = DespesasSerializer
