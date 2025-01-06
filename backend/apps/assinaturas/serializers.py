# Módulo Assinaturas - Serializers (serializers.py)

from rest_framework import serializers
from .models import Documento, Assinatura
from django.utils import timezone


class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = "__all__"
        read_only_fields = [
            "uuid",
            "data_criacao",
            "data_atualizacao",
            "hash_documento",
            "versao",
            "analise_automatizada",
        ]

    def validate(self, data):
        # Validação para garantir que a data de expiração não seja anterior à
        # data atual
        if "data_expiracao" in data and data["data_expiracao"]:
            if data["data_expiracao"] < timezone.now().date():
                raise serializers.ValidationError(
                    "A data de expiração não pode ser anterior à data atual."
                )
        # Validação de conformidade regulamentar
        if not data.get("compliance_regulamentar"):
            raise serializers.ValidationError(
                "É necessário especificar a conformidade regulamentar para garantir que o documento atende aos padrões legais."
            )
        # Validação de interoperabilidade
        if data.get("associado_prontuario") and not data.get("paciente"):
            raise serializers.ValidationError(
                "Documentos associados ao prontuário devem estar vinculados a um paciente."
            )
        return data

    def create(self, validated_data):
        # Lógica adicional ao criar um documento, como definir a expiração
        # padrão e gerar o hash
        documento = super().create(validated_data)
        documento.definir_expiracao_padrao()
        documento.gerar_hash_documento()
        return documento

    def update(self, instance, validated_data):
        # Atualiza a versão do documento ao fazer alterações
        instance.versao += 1
        instance = super().update(instance, validated_data)
        instance.gerar_hash_documento()
        return instance


class AssinaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assinatura
        fields = "__all__"
        read_only_fields = [
            "uuid",
            "data_assinatura",
            "assinatura_eletronica",
            "historico_eventos",
        ]

    def validate(self, data):
        # Validação para garantir que a assinatura eletrônica tenha integridade
        if data.get("documento") and data.get("assinante"):
            documento = data["documento"]
            if documento.is_expired():
                raise serializers.ValidationError(
                    "Não é possível assinar um documento expirado."
                )
            # Validação de dupla autenticação
            if documento.consentimento_informado and not data.get("dupla_autenticacao"):
                raise serializers.ValidationError(
                    "Documentos que exigem consentimento informado precisam de autenticação em duas etapas."
                )
        # Verificação de integridade de assinatura com hash
        if data.get("assinatura_eletronica") and data.get("biometria_hash"):
            if not self.validar_integridade_assinatura(
                data["assinatura_eletronica"], data["biometria_hash"]
            ):
                raise serializers.ValidationError(
                    "A integridade da assinatura não foi confirmada."
                )
        return data

    def create(self, validated_data):
        # Lógica para gerar assinatura eletrônica ao criar uma assinatura
        assinatura = super().create(validated_data)
        assinatura.gerar_assinatura_eletronica()
        assinatura.registrar_evento("Assinatura criada.")
        return assinatura

    def update(self, instance, validated_data):
        # Lógica adicional ao atualizar uma assinatura
        instance = super().update(instance, validated_data)
        instance.registrar_evento("Assinatura atualizada.")
        return instance

    def validar_integridade_assinatura(self, assinatura_eletronica, biometria_hash):
        # Lógica simulada para validar a integridade da assinatura com base no hash armazenado
        # (Aqui pode ser feita uma validação mais complexa em um serviço externo)
        return True
