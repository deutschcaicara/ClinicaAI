from rest_framework import viewsets
from .models import Profissionai
from .serializers import ProfissionaiSerializer

class ProfissionaiViewSet(viewsets.ModelViewSet):
    queryset = Profissionai.objects.all()
    serializer_class = ProfissionaiSerializer
