from rest_framework import serializers
from .models import DocumentosModel


class DocumentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentosModel
        fields = "__all__"
