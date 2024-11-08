from rest_framework import viewsets
from .models import BlogModel
from .serializers import BlogSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = BlogModel.objects.all()
    serializer_class = BlogSerializer
