from rest_framework import viewsets
from .models import CrmModel
from .serializers import CrmSerializer

class CrmViewSet(viewsets.ModelViewSet):
    queryset = CrmModel.objects.all()
    serializer_class = CrmSerializer
