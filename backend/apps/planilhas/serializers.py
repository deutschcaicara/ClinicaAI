from rest_framework import serializers
from .models import PlanilhasModel

class PlanilhasSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanilhasModel
        fields = '__all__'
