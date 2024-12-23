# Incremento 4: Melhorias no Módulo de Testes (tests.py)

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Paciente


class PacienteTests(APITestCase):
    def setUp(self):
        # Criação de usuário para autenticação
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        # Dados do paciente para testes
        self.paciente_data = {
            "nome_completo": "João da Silva",
            "cpf": "123.456.789-00",
            "data_nascimento": "1980-01-01",
            "sexo": "M",
            "estado_civil": "Solteiro",
            "endereco": "Rua A",
            "numero": "123",
            "bairro": "Centro",
            "cidade": "São Paulo",
            "estado": "SP",
            "telefone_celular": "(11) 91234-5678",
            "email": "joao.silva@example.com",
            "consentimento_lgpd": True,
        }

    def test_create_paciente_unauthorized(self):
        # Tentativa de criação de paciente sem ser administrador
        response = self.client.post(reverse("paciente-list"), self.paciente_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_paciente_authorized(self):
        # Criação de paciente como administrador
        self.client.login(username="admin", password="adminpassword")
        response = self.client.post(reverse("paciente-list"), self.paciente_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Paciente.objects.count(), 1)
        self.assertEqual(Paciente.objects.get().nome_completo, "João da Silva")

    def test_list_pacientes(self):
        # Listar pacientes após criação
        self.client.login(username="admin", password="adminpassword")
        self.client.post(reverse("paciente-list"), self.paciente_data)
        response = self.client.get(reverse("paciente-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_permissions(self):
        # Verificar permissões de acesso para listagem
        response = self.client.get(reverse("paciente-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        response = self.client.get(reverse("paciente-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
