from rest_framework import serializers
from .models import FolgasModel

class FolgasSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolgasModel
        fields = '__all__'
