from rest_framework import serializers
from .models import QualidadeModel


class QualidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualidadeModel
        fields = "__all__"
