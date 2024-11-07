# Incremento 2: Melhorias no Serializador (serializers.py)

from rest_framework import serializers
from .models import Paciente
from django.core.validators import validate_email
import re

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            'uuid', 'nome_completo', 'foto', 'data_nascimento', 'sexo', 'estado_civil', 'profissao',
            'nacionalidade', 'naturalidade', 'endereco', 'numero', 'complemento', 'bairro', 'cidade',
            'estado', 'cep', 'telefone_residencial', 'telefone_celular', 'email',
            'contato_emergencia', 'telefone_emergencia', 'nome_mae', 'nome_pai',
            'consentimento_lgpd', 'observacoes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_cpf(self, value):
        # Validação simples de CPF (apenas para garantir formato válido)
        if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', value):
            raise serializers.ValidationError("CPF deve estar no formato XXX.XXX.XXX-XX")
        return value

    def validate_email(self, value):
        # Validação de e-mail
        try:
            validate_email(value)
        except:
            raise serializers.ValidationError("E-mail inválido")
        return value
