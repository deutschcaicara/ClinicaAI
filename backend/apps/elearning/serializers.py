from rest_framework import serializers
from .models import ElearningModel


class ElearningSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElearningModel
        fields = "__all__"
