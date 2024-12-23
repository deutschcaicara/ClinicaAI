# Módulo Profissionais - Serializers (serializers.py)

from rest_framework import serializers
from apps.profissionais.models import (
    Especialidade,
    Profissional,
    Disponibilidade,
    RegistroHorasTrabalhadas,
)


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = "__all__"


class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = "__all__"


class DisponibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilidade
        fields = "__all__"


class RegistroHorasTrabalhadasSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroHorasTrabalhadas
        fields = "__all__"
