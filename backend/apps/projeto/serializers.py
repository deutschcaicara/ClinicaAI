from rest_framework import serializers
from .models import ProjetoModel


class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjetoModel
        fields = "__all__"
