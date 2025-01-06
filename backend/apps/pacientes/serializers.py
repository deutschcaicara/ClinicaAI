from rest_framework import serializers
from .models import Paciente
from django.core.validators import validate_email
import re
from apps.prontuarios.serializers import ProntuarioSerializer

class PacienteSerializer(serializers.ModelSerializer):
    cpf = serializers.SerializerMethodField()
    rg = serializers.SerializerMethodField()
    prontuario = ProntuarioSerializer(read_only=True)

    class Meta:
        model = Paciente
        fields = [
            "uuid",
            "nome_completo",
            "foto",
            "cpf",
            "rg",
            "data_nascimento",
            "sexo",
            "estado_civil",
            "profissao",
            "nacionalidade",
            "naturalidade",
            "endereco",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
            "cep",
            "telefone_residencial",
            "telefone_celular",
            "email",
            "contato_emergencia",
            "telefone_emergencia",
            "nome_mae",
            "nome_pai",
            "consentimento_lgpd",
            "observacoes",
            "created_at",
            "updated_at",
            "prontuario",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_cpf(self, obj):
        return obj.decrypt_cpf()

    def get_rg(self, obj):
        return obj.decrypt_rg()

    def validate_cpf(self, value):
        if not value or value.strip() == "":
          raise serializers.ValidationError("CPF não pode estar vazio.")
        if not re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", value):
            raise serializers.ValidationError("CPF deve estar no formato XXX.XXX.XXX-XX.")
        return value

    
    def validate_email(self, value):
        # Validação de e-mail
        try:
            validate_email(value)
        except Exception:
            raise serializers.ValidationError("E-mail inválido")
        return value
