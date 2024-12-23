from rest_framework import serializers
from .models import Assinar_documentosModel


class Assinar_documentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assinar_documentosModel
        fields = "__all__"
