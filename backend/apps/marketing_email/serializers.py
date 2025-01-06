from rest_framework import serializers
from .models import Marketing_emailModel


class Marketing_emailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketing_emailModel
        fields = "__all__"
