from rest_framework import serializers
from .models import Marketing_smsModel

class Marketing_smsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketing_smsModel
        fields = '__all__'
