from rest_framework import serializers
from .models import IndicacoesModel


class IndicacoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicacoesModel
        fields = "__all__"
