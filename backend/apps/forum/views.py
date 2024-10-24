from rest_framework import viewsets
from .models import ForumModel
from .serializers import ForumSerializer

class ForumViewSet(viewsets.ModelViewSet):
    queryset = ForumModel.objects.all()
    serializer_class = ForumSerializer
