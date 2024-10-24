from rest_framework import viewsets
from .models import EcommerceModel
from .serializers import EcommerceSerializer

class EcommerceViewSet(viewsets.ModelViewSet):
    queryset = EcommerceModel.objects.all()
    serializer_class = EcommerceSerializer
