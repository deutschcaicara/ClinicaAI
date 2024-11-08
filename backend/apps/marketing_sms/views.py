from rest_framework import viewsets
from .models import Marketing_smsModel
from .serializers import Marketing_smsSerializer


class Marketing_smsViewSet(viewsets.ModelViewSet):
    queryset = Marketing_smsModel.objects.all()
    serializer_class = Marketing_smsSerializer
