from rest_framework import serializers
from .models import DespesasModel


class DespesasSerializer(serializers.ModelSerializer):
    class Meta:
        model = DespesasModel
        fields = "__all__"
