from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Transacao, Fatura, Orcamento

class FinanceiroTests(APITestCase):
    def setUp(self):
        # Criar superusuário para autenticação
        self.user = User.objects.create_superuser(username="admin", password="adminpassword")

        # Gerar token JWT
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        # Configurar o cabeçalho de autorização para usar o token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Dados iniciais para os testes
        self.transacao_data = {
            "descricao": "Consulta",
            "valor": 100.00,
            "tipo": "receita",
            "categoria": "consulta",
        }
        self.fatura_data = {
            "vencimento": "2025-01-10",
            "valor": 100.00,
            "meio_pagamento": "pix",
        }
        self.orcamento_data = {
            "centro_custo": "Radiologia",
            "periodo_inicio": "2025-01-01",
            "periodo_fim": "2025-12-31",
            "valor_planejado": 50000.00,
        }

    def test_create_transacao(self):
        response = self.client.post(reverse('transacao-list'), self.transacao_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_fatura(self):
        response = self.client.post(reverse('fatura-list'), self.fatura_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_orcamento(self):
        response = self.client.post(reverse('orcamento-list'), self.orcamento_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
