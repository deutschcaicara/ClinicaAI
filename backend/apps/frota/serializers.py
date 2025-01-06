from rest_framework import serializers
from .models import FrotaModel


class FrotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrotaModel
        fields = "__all__"
