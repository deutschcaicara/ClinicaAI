import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.financeiro.models import Conta, Renegociacao, CategoriaFinanceira
from datetime import date

@pytest.mark.django_db
class TestContaAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="admin", password="password")
        self.client.force_authenticate(user=self.user)
        self.categoria = CategoriaFinanceira.objects.create(nome="Categoria Teste")

    def test_criar_conta(self):
        payload = {
            "descricao": "Conta Teste",
            "tipo": "pagar",
            "valor": 200.00,
            "vencimento": str(date.today()),
            "status": "pendente",
            "categoria": self.categoria.id,
        }
        response = self.client.post("/api/financeiro/contas/", payload)
        assert response.status_code == 201
        assert response.data["descricao"] == "Conta Teste"

    def test_listar_contas(self):
        Conta.objects.create(descricao="Conta 1", tipo="pagar", valor=100.00, vencimento=date.today(), categoria=self.categoria)
        Conta.objects.create(descricao="Conta 2", tipo="receber", valor=150.00, vencimento=date.today(), categoria=self.categoria)
        response = self.client.get("/api/financeiro/contas/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_renegociar_conta(self):
        conta = Conta.objects.create(descricao="Conta Antiga", tipo="pagar", valor=200.00, vencimento=date.today(), categoria=self.categoria)
        payload = {
            "novo_valor": 180.00,
            "nova_data_vencimento": str(date.today()),
            "condicoes": "Desconto aplicado na renegociação."
        }
        response = self.client.post(f"/api/financeiro/contas/{conta.id}/renegociar/", payload)
        assert response.status_code == 200
        renegociacao = Renegociacao.objects.filter(conta=conta).first()
        assert renegociacao.novo_valor == 180.00
