from rest_framework import serializers
from .models import EcommerceModel

class EcommerceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcommerceModel
        fields = '__all__'
