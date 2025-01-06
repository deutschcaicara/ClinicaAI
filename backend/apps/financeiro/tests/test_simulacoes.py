import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.financeiro.models import Orcamento, SimulacaoCenario
from datetime import date

@pytest.mark.django_db
class TestSimulacaoCenarioAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="admin", password="password")
        self.client.force_authenticate(user=self.user)
        self.orcamento = Orcamento.objects.create(
            centro_custo="Centro Teste", periodo_inicio=date.today(), periodo_fim=date.today(), valor_planejado=1000.00
        )

    def test_criar_simulacao(self):
        payload = {
            "nome": "Simulação Teste",
            "descricao": "Teste de impacto financeiro.",
            "orcamento": self.orcamento.id,
            "impacto_receitas": 200.00,
            "impacto_despesas": 100.00,
        }
        response = self.client.post("/api/financeiro/simulacoes/", payload)
        assert response.status_code == 201
        assert response.data["nome"] == "Simulação Teste"

    def test_listar_simulacoes(self):
        SimulacaoCenario.objects.create(nome="Simulação 1", orcamento=self.orcamento, impacto_receitas=300.00, impacto_despesas=150.00)
        response = self.client.get("/api/financeiro/simulacoes/")
        assert response.st
