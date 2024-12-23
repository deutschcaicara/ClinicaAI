from rest_framework import serializers
from .models import CrmModel


class CrmSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrmModel
        fields = "__all__"
