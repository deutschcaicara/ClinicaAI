from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    CategoriaFinanceira,
    LogAuditoria,
    RelatorioFinanceiro,
    SimulacaoCenario,
    Orcamento,
    Conta,
    Transacao,
)
from .serializers import (
    CategoriaFinanceiraSerializer,
    LogAuditoriaSerializer,
    RelatorioFinanceiroSerializer,
    SimulacaoCenarioSerializer,
    OrcamentoSerializer,
    ContaSerializer,
    TransacaoSerializer,
)


class CategoriaFinanceiraViewSet(viewsets.ModelViewSet):
    queryset = CategoriaFinanceira.objects.all()
    serializer_class = CategoriaFinanceiraSerializer
    filterset_fields = ["ativa", "nome"]
    search_fields = ["nome", "descricao"]
    ordering_fields = ["nome"]
    ordering = ["nome"]
    
class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tipo", "categoria", "status", "forma_pagamento", "data"]
    search_fields = ["descricao", "tags"]
    ordering_fields = ["data", "valor"]
    ordering = ["-data"]

class ContaViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    filterset_fields = ["tipo", "status", "vencimento", "categoria"]
    search_fields = ["descricao"]
    ordering_fields = ["vencimento", "valor"]
    ordering = ["-vencimento"]

    @action(detail=True, methods=["post"])
    def renegociar(self, request, pk=None):
        conta = self.get_object()
        novo_valor = request.data.get("novo_valor")
        nova_data_vencimento = request.data.get("nova_data_vencimento")
        condicoes = request.data.get("condicoes", "")
        if not novo_valor or not nova_data_vencimento:
            return Response({"erro": "Os campos 'novo_valor' e 'nova_data_vencimento' são obrigatórios."},
                            status=status.HTTP_400_BAD_REQUEST)
        conta.status = "renegociado"
        conta.save()
        conta.renegociacoes.create(
            novo_valor=novo_valor,
            nova_data_vencimento=nova_data_vencimento,
            condicoes=condicoes
        )
        return Response({"status": "Conta renegociada com sucesso."})
class OrcamentoViewSet(viewsets.ModelViewSet):
    queryset = Orcamento.objects.all()
    serializer_class = OrcamentoSerializer
    filterset_fields = ["centro_custo", "periodo_inicio", "periodo_fim"]
    ordering_fields = ["periodo_inicio", "periodo_fim"]
    ordering = ["-periodo_inicio"]

class SimulacaoCenarioViewSet(viewsets.ModelViewSet):
    queryset = SimulacaoCenario.objects.all()
    serializer_class = SimulacaoCenarioSerializer
    filterset_fields = ["orcamento"]
    ordering_fields = ["criado_em"]
    ordering = ["-criado_em"]
    
class RelatorioFinanceiroViewSet(viewsets.ModelViewSet):
    queryset = RelatorioFinanceiro.objects.all()
    serializer_class = RelatorioFinanceiroSerializer
    filterset_fields = ["tipo", "periodo_inicio", "periodo_fim"]
    ordering_fields = ["criado_em"]
    ordering = ["-criado_em"]
    
class LogAuditoriaViewSet(viewsets.ModelViewSet):
    queryset = LogAuditoria.objects.all()
    serializer_class = LogAuditoriaSerializer
    filterset_fields = ["usuario", "acao"]
    ordering_fields = ["data_hora"]
    ordering = ["-data_hora"]