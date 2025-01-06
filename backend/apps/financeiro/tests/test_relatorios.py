import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.financeiro.models import RelatorioFinanceiro
from datetime import date

@pytest.mark.django_db
class TestRelatorioFinanceiroAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="admin", password="password")
        self.client.force_authenticate(user=self.user)

    def test_criar_relatorio(self):
        payload = {
            "tipo": "Relatório Teste",
            "descricao": "Relatório financeiro gerado automaticamente.",
            "periodo_inicio": str(date.today()),
            "periodo_fim": str(date.today()),
            "conteudo": {"receitas": 1000, "despesas": 500, "saldo": 500},
        }
        response = self.client.post("/api/financeiro/relatorios/", payload)
        assert response.status_code == 201
        assert response.data["tipo"] == "Relatório Teste"
