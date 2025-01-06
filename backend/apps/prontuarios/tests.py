from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import (
    Prontuario,
    HistoricoMedicamentos,
    EvolucaoClinica,
    DadosVitais,
    HistoricoAcessosProntuario,
    ExameComplementar,
)


class ProntuarioAPITestCase(APITestCase):
    def setUp(self):
        # Criação de usuários e grupos para testar permissões
        self.admin_user = User.objects.create_superuser(
            "admin", "admin@example.com", "password123"
        )
        self.doctor_user = User.objects.create_user(
            "doctor", "doctor@example.com", "password123"
        )
        doctor_group, created = Group.objects.get_or_create(name="Doctor")
        self.doctor_user.groups.add(doctor_group)
        self.patient_user = User.objects.create_user(
            "patient", "patient@example.com", "password123"
        )

        # Criação de dados iniciais
        self.prontuario = Prontuario.objects.create(paciente_id=1)

    def test_create_prontuario_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"paciente": 1, "queixa_principal": "Dor de cabeça persistente"}
        response = self.client.post(reverse("prontuarios-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_prontuario_as_patient(self):
        self.client.force_authenticate(user=self.patient_user)
        data = {"paciente": 1, "queixa_principal": "Dor de cabeça persistente"}
        response = self.client.post(reverse("prontuarios-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_prontuarios_as_doctor(self):
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.get(reverse("prontuarios-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HistoricoMedicamentosAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            "admin", "admin@example.com", "password123"
        )
        self.doctor_user = User.objects.create_user(
            "doctor", "doctor@example.com", "password123"
        )
        doctor_group, created = Group.objects.get_or_create(name="Doctor")
        self.doctor_user.groups.add(doctor_group)
        self.patient_user = User.objects.create_user(
            "patient", "patient@example.com", "password123"
        )

        # Criação de dados iniciais
        self.medicamento = HistoricoMedicamentos.objects.create(
            prontuario_id=1, medicamento="Paracetamol", dosagem="500mg"
        )

    def test_create_medicamento_as_doctor(self):
        self.client.force_authenticate(user=self.doctor_user)
        data = {"prontuario": 1, "medicamento": "Ibuprofeno", "dosagem": "400mg"}
        response = self.client.post(reverse("historico_medicamentos-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_medicamento_as_patient(self):
        self.client.force_authenticate(user=self.patient_user)
        data = {"medicamento": "Aspirina"}
        response = self.client.patch(
            reverse("historico_medicamentos-detail", args=[self.medicamento.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EvolucaoClinicaAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            "admin", "admin@example.com", "password123"
        )
        self.doctor_user = User.objects.create_user(
            "doctor", "doctor@example.com", "password123"
        )
        doctor_group, created = Group.objects.get_or_create(name="Doctor")
        self.doctor_user.groups.add(doctor_group)

        # Criação de dados iniciais
        self.evolucao = EvolucaoClinica.objects.create(
            prontuario_id=1, descricao="Paciente com sintomas de gripe"
        )

    def test_update_evolucao_as_doctor(self):
        self.client.force_authenticate(user=self.doctor_user)
        data = {"descricao": "Paciente com febre alta e tosse"}
        response = self.client.patch(
            reverse("evolucoes_clinicas-detail", args=[self.evolucao.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_evolucao_as_patient(self):
        self.client.force_authenticate(user=self.patient_user)
        data = {"descricao": "Tentativa de atualização não permitida"}
        response = self.client.patch(
            reverse("evolucoes_clinicas-detail", args=[self.evolucao.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DadosVitaisAPITestCase(APITestCase):
    def setUp(self):
        self.doctor_user = User.objects.create_user(
            "doctor", "doctor@example.com", "password123"
        )
        doctor_group, created = Group.objects.get_or_create(name="Doctor")
        self.doctor_user.groups.add(doctor_group)

        # Criação de dados iniciais
        self.dados_vitais = DadosVitais.objects.create(
            prontuario_id=1, pressao_arterial="120/80"
        )

    def test_create_dados_vitais_as_doctor(self):
        self.client.force_authenticate(user=self.doctor_user)
        data = {
            "prontuario": 1,
            "pressao_arterial": "130/85",
            "frequencia_cardiaca": "75",
        }
        response = self.client.post(reverse("dados_vitais-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_dados_vitais_as_unauthorized_user(self):
        unauthorized_user = User.objects.create_user(
            "unauthorized", "unauthorized@example.com", "password123"
        )
        self.client.force_authenticate(user=unauthorized_user)
        data = {"prontuario": 1, "pressao_arterial": "130/85"}
        response = self.client.post(reverse("dados_vitais-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
