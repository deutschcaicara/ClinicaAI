from rest_framework import serializers
from .models import CompromissosModel

class CompromissosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompromissosModel
        fields = '__all__'
