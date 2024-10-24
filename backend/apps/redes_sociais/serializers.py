from rest_framework import serializers
from .models import Redes_sociaisModel

class Redes_sociaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redes_sociaisModel
        fields = '__all__'
