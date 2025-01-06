from rest_framework import serializers
from .models import AvaliacoesModel


class AvaliacoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvaliacoesModel
        fields = "__all__"
