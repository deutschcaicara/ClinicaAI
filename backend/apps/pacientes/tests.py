from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Paciente
from rest_framework_simplejwt.tokens import RefreshToken

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
# Gerar token para o admin
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        # Dados do paciente para testes
        self.paciente_data = {
            "nome_completo": "João da Silva",
            "cpf": "123.456.789-00",
            "rg": "MG-12.345.678",
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

    def test_create_paciente(self):
        response = self.client.post(reverse("paciente-list"), self.paciente_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_paciente_unauthorized(self):
        self.client.credentials()  # Remove o token
        response = self.client.post(reverse("paciente-list"), self.paciente_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_duplicate_cpf(self):
        # Testar duplicidade de CPF
        response = self.client.post(reverse("paciente-list"), self.paciente_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Alterar o CPF no segundo teste
        duplicate_data = self.paciente_data.copy()
        duplicate_data["cpf"] = "987.654.321-00"  # CPF diferente
        response = self.client.post(reverse("paciente-list"), duplicate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_required_fields(self):
        invalid_data = self.paciente_data.copy()
        invalid_data.pop("cpf")  # Remove CPF
        response = self.client.post(reverse("paciente-list"), invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_descriptografia_campos(self):
        # Verificar se CPF e RG são descriptografados corretamente
        self.client.login(username="admin", password="adminpassword")
        response = self.client.post(reverse("paciente-list"), self.paciente_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        paciente_id = response.data["uuid"]
        response = self.client.get(reverse("paciente-detail", args=[paciente_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["cpf"], "123.456.789-00")
        self.assertEqual(response.data["rg"], "MG-12.345.678")
