from rest_framework import serializers
from .models import Criador_sitesModel


class Criador_sitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criador_sitesModel
        fields = "__all__"
