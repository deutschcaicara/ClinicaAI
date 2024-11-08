from rest_framework import serializers
from .models import VendasModel


class VendasSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendasModel
        fields = "__all__"
