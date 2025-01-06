import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.financeiro.models import Transacao, CategoriaFinanceira

@pytest.mark.django_db
class TestTransacaoAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="admin", password="password")
        self.client.force_authenticate(user=self.user)
        self.categoria = CategoriaFinanceira.objects.create(nome="Categoria Teste")

    def test_criar_transacao(self):
        payload = {
            "descricao": "Transação Teste",
            "valor": 100.00,
            "tipo": "receita",
            "categoria": self.categoria.id,
        }
        response = self.client.post("/api/financeiro/transacoes/", payload)
        assert response.status_code == 201
        assert response.data["descricao"] == "Transação Teste"

    def test_listar_transacoes(self):
        Transacao.objects.create(descricao="Transação 1", valor=50.00, tipo="receita", categoria=self.categoria)
        Transacao.objects.create(descricao="Transação 2", valor=100.00, tipo="despesa", categoria=self.categoria)
        response = self.client.get("/api/financeiro/transacoes/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_filtrar_transacoes_por_tipo(self):
        Transacao.objects.create(descricao="Receita", valor=150.00, tipo="receita", categoria=self.categoria)
        Transacao.objects.create(descricao="Despesa", valor=50.00, tipo="despesa", categoria=self.categoria)
        response = self.client.get("/api/financeiro/transacoes/?tipo=receita")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["descricao"] == "Receita"
