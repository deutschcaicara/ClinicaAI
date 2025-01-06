from rest_framework import serializers
from .models import Planilhas_horasModel


class Planilhas_horasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planilhas_horasModel
        fields = "__all__"
