from rest_framework import serializers
from .models import ForumModel

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumModel
        fields = '__all__'
