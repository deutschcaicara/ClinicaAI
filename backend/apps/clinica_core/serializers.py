from rest_framework import serializers
from .models import LogSistema, Documento

class LogSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSistema
        fields = "__all__"

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = "__all__"
