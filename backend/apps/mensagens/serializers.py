from rest_framework import serializers
from .models import MensagensModel


class MensagensSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensagensModel
        fields = "__all__"
