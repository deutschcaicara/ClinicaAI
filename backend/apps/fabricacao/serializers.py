from rest_framework import serializers
from .models import FabricacaoModel


class FabricacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FabricacaoModel
        fields = "__all__"
