from rest_framework import viewsets
from .models import AssinaturasModel
from .serializers import AssinaturasSerializer

class AssinaturasViewSet(viewsets.ModelViewSet):
    queryset = AssinaturasModel.objects.all()
    serializer_class = AssinaturasSerializer
