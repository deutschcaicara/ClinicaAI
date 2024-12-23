from rest_framework import serializers
from .models import RecrutamentoModel


class RecrutamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecrutamentoModel
        fields = "__all__"
