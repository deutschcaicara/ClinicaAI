# Arquivo: /mnt/dados/clinicaai/pacientes/serializers.py

from rest_framework import serializers
from .models.paciente import Paciente
from .models.consulta import Consulta
from .models.exame import Exame

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'

class ExameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exame
        fields = '__all__'
