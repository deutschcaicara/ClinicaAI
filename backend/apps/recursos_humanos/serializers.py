from rest_framework import serializers
from .models import Recursos_humanosModel


class Recursos_humanosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recursos_humanosModel
        fields = "__all__"
