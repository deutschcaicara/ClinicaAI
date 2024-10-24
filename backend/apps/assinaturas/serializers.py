from rest_framework import serializers
from .models import AssinaturasModel

class AssinaturasSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssinaturasModel
        fields = '__all__'
