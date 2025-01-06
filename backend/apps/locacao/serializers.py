from rest_framework import serializers
from .models import LocacaoModel


class LocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocacaoModel
        fields = "__all__"
