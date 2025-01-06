import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.financeiro.models import CategoriaFinanceira

@pytest.mark.django_db
class TestCategoriaFinanceiraAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="admin", password="password")
        self.client.force_authenticate(user=self.user)

    def test_criar_categoria(self):
        payload = {"nome": "Categoria Teste", "descricao": "Descrição da categoria"}
        response = self.client.post("/api/financeiro/categorias/", payload)
        assert response.status_code == 201
        assert response.data["nome"] == "Categoria Teste"

    def test_listar_categorias(self):
        CategoriaFinanceira.objects.create(nome="Categoria 1")
        CategoriaFinanceira.objects.create(nome="Categoria 2")
        response = self.client.get("/api/financeiro/categorias/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_atualizar_categoria(self):
        categoria = CategoriaFinanceira.objects.create(nome="Categoria Antiga")
        payload = {"nome": "Categoria Atualizada"}
        response = self.client.put(f"/api/financeiro/categorias/{categoria.id}/", payload)
        assert response.status_code == 200
        assert response.data["nome"] == "Categoria Atualizada"

    def test_remover_categoria(self):
        categoria = CategoriaFinanceira.objects.create(nome="Categoria Removida")
        response = self.client.delete(f"/api/financeiro/categorias/{categoria.id}/")
        assert response.status_code == 204
        assert not CategoriaFinanceira.objects.filter(id=categoria.id).exists()
