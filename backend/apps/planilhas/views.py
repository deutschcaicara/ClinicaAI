from rest_framework import viewsets
from .models import PlanilhasModel
from .serializers import PlanilhasSerializer


class PlanilhasViewSet(viewsets.ModelViewSet):
    queryset = PlanilhasModel.objects.all()
    serializer_class = PlanilhasSerializer
