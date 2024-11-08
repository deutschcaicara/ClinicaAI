from rest_framework import viewsets
from .models import Marketing_emailModel
from .serializers import Marketing_emailSerializer


class Marketing_emailViewSet(viewsets.ModelViewSet):
    queryset = Marketing_emailModel.objects.all()
    serializer_class = Marketing_emailSerializer
