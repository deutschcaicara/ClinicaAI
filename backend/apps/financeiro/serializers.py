from rest_framework import serializers
from .models import CategoriaFinanceira, Transacao, Orcamento, SimulacaoCenario, RelatorioFinanceiro, LogAuditoria,Conta, Renegociacao


class CategoriaFinanceiraSerializer(serializers.ModelSerializer):
    subcategoria = serializers.StringRelatedField()

    class Meta:
        model = CategoriaFinanceira
        fields = ["id", "nome", "descricao", "subcategoria", "ativa"]
class TransacaoSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField()
    forma_pagamento_display = serializers.CharField(source="get_forma_pagamento_display", read_only=True)

    class Meta:
        model = Transacao
        fields = [
            "id", "descricao", "valor", "tipo", "forma_pagamento", "forma_pagamento_display", 
            "categoria", "tags", "data", "paciente", "fornecedor", "centro_custo", 
            "anexos", "status", "categoria_sugerida", "criado_em", "criado_por", "atualizado_em", "atualizado_por"
        ]
        read_only_fields = ["criado_em", "criado_por", "atualizado_em", "atualizado_por"]


class ContaSerializer(serializers.ModelSerializer):
    impacto_fluxo_caixa = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Conta
        fields = [
            "id", "descricao", "tipo", "valor", "vencimento", "status", "status_display", 
            "fornecedor", "cliente", "categoria", "parcelada", "numero_parcelas", 
            "parcela_atual", "juros", "multa", "desconto", "impacto_fluxo_caixa", 
            "criado_em", "criado_por", "atualizado_em", "atualizado_por"
        ]
class RenegociacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renegociacao
        fields = ["id", "conta", "data_renegociacao", "novo_valor", "nova_data_vencimento", "condicoes"]

class OrcamentoSerializer(serializers.ModelSerializer):
    percentual_gasto = serializers.SerializerMethodField()

    class Meta:
        model = Orcamento
        fields = ["id", "centro_custo", "periodo_inicio", "periodo_fim", "valor_planejado", "valor_gasto", "percentual_gasto"]

    def get_percentual_gasto(self, obj):
        if obj.valor_planejado > 0:
            return (obj.valor_gasto / obj.valor_planejado) * 100
        return 0
class SimulacaoCenarioSerializer(serializers.ModelSerializer):
    saldo_simulado = serializers.SerializerMethodField()

    class Meta:
        model = SimulacaoCenario
        fields = ["id", "nome", "descricao", "orcamento", "impacto_receitas", "impacto_despesas", "saldo_simulado"]

    def get_saldo_simulado(self, obj):
        saldo_atual = obj.orcamento.valor_planejado - obj.orcamento.valor_gasto
        return saldo_atual + obj.impacto_receitas - obj.impacto_despesas
class RelatorioFinanceiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatorioFinanceiro
        fields = ["id", "tipo", "descricao", "periodo_inicio", "periodo_fim", "conteudo", "exportado", "formato_exportado"]
class LogAuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAuditoria
        fields = ["id", "usuario", "acao", "data_hora", "detalhes", "ip_origem"]
