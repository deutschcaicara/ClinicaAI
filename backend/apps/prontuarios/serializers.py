# Módulo Prontuários - Serializers (serializers.py)

from rest_framework import serializers
from .models import (
    Prontuario,
    HistoricoMedicamentos,
    EvolucaoClinica,
    DadosVitais,
    HistoricoAcessosProntuario,
    ExameComplementar,
    Anamnese,
)


class ProntuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prontuario
        fields = "__all__"


class HistoricoMedicamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoMedicamentos
        fields = "__all__"


class EvolucaoClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvolucaoClinica
        fields = "__all__"


class DadosVitaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosVitais
        fields = "__all__"


class HistoricoAcessosProntuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoAcessosProntuario
        fields = "__all__"


class ExameComplementarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExameComplementar
        fields = "__all__"


class AnamneseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anamnese
        fields = '__all__'