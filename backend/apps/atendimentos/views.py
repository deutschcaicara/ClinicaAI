from rest_framework import viewsets
from .models import Atendimento
from .serializers import AtendimentoSerializer

class AtendimentoViewSet(viewsets.ModelViewSet):
    queryset = Atendimento.objects.all()
    serializer_class = AtendimentoSerializer
