from rest_framework import serializers
from .models import Exame

class ExameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exame
        fields = '__all__'
