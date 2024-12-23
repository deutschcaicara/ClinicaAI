from rest_framework import serializers
from .models import ComprasModel


class ComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprasModel
        fields = "__all__"
