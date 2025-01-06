from rest_framework import serializers
from .models import FaturamentoModel


class FaturamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaturamentoModel
        fields = "__all__"
