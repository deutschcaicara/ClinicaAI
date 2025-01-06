from rest_framework import serializers
from .models import PlmModel


class PlmSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlmModel
        fields = "__all__"
