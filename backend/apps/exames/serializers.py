# Módulo Exames - Serializers (serializers.py)

from rest_framework import serializers
from .models import Exame


class ExameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exame
        fields = "__all__"
        read_only_fields = ["data_criacao", "data_atualizacao"]

    def validate(self, data):
        # Validação para garantir que a data de realização não seja anterior à
        # data de solicitação
        if "data_realizacao" in data and data["data_realizacao"]:
            if data["data_realizacao"] < data["data_solicitacao"]:
                raise serializers.ValidationError(
                    "A data de realização não pode ser anterior à data de solicitação do exame."
                )

        # Validação para garantir que se o exame estiver realizado, a data de
        # realização deve estar preenchida
        if data.get("status") == "Realizado" and not data.get("data_realizacao"):
            raise serializers.ValidationError(
                "A data de realização deve ser informada quando o status for 'Realizado'."
            )

        # Validação para garantir que se o exame estiver realizado, o documento
        # do resultado deve estar presente
        if data.get("status") == "Realizado" and not data.get("documento_resultado"):
            raise serializers.ValidationError(
                "O documento do resultado deve ser anexado quando o status for 'Realizado'."
            )

        return data
