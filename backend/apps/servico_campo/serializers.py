from rest_framework import serializers
from .models import Servico_campoModel


class Servico_campoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico_campoModel
        fields = "__all__"
