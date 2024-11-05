from rest_framework import serializers
from .models import Profissionai

class ProfissionaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissionai
        fields = '__all__'
