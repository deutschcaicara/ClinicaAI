from rest_framework import serializers
from .models import ManutencaoModel

class ManutencaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManutencaoModel
        fields = '__all__'
