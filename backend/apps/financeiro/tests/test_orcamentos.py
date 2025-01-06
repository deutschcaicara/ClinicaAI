import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.financeiro.models import Orcamento
from datetime import date

@pytest.mark.django_db
class TestOrcamentoAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="admin", password="password")
        self.client.force_authenticate(user=self.user)

    def test_criar_orcamento(self):
        payload = {
            "centro_custo": "Centro de Teste",
            "periodo_inicio": str(date.today()),
            "periodo_fim": str(date.today()),
            "valor_planejado": 1000.00,
            "valor_gasto": 200.00,
        }
        response = self.client.post("/api/financeiro/orcamentos/", payload)
        assert response.status_code == 201
        assert response.data["centro_custo"] == "Centro de Teste"

    def test_listar_orcamentos(self):
        Orcamento.objects.create(centro_custo="Centro 1", periodo_inicio=date.today(), periodo_fim=date.today(), valor_planejado=500.00)
        Orcamento.objects.create(centro_custo="Centro 2", periodo_inicio=date.today(), periodo_fim=date.today(), valor_planejado=800.00)
        response = self.client.get("/api/financeiro/orcamentos/")
        assert response.status_code == 200
        assert len(response.data) == 2
