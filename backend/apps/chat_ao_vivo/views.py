from rest_framework import viewsets
from .models import Chat_ao_vivoModel
from .serializers import Chat_ao_vivoSerializer


class Chat_ao_vivoViewSet(viewsets.ModelViewSet):
    queryset = Chat_ao_vivoModel.objects.all()
    serializer_class = Chat_ao_vivoSerializer
