# Módulo Atendimentos - Tests (tests.py)

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Atendimento
from apps.pacientes.models import Paciente

from apps.profissionais.models import Profissional
import Profissional
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
from unittest.mock import patch

User = get_user_model()


class AtendimentoAPITestCase(APITestCase):
    def setUp(self):
        # Configurar usuários, paciente, profissional e atendimento para os
        # testes
        self.client = APIClient()
        self.user_paciente = User.objects.create_user(
            username="paciente", password="testpassword"
        )
        self.paciente = Paciente.objects.create(
            usuario=self.user_paciente, nome_completo="Paciente Teste"
        )

        self.user_profissional = User.objects.create_user(
            username="profissional", password="testpassword"
        )
        self.profissional = Profissional.objects.create(
            usuario=self.user_profissional, nome_completo="Profissional Teste"
        )

        self.user_outro_profissional = User.objects.create_user(
            username="outro_profissional", password="testpassword"
        )
        self.outro_profissional = Profissional.objects.create(
            usuario=self.user_outro_profissional,
            nome_completo="Outro Profissional Teste",
        )

        self.atendimento = Atendimento.objects.create(
            uuid=uuid.uuid4(),
            paciente=self.paciente,
            profissional=self.profissional,
            data_atendimento=timezone.now().date() + timezone.timedelta(days=1),
            horario_inicio="10:00",
            horario_fim="11:00",
            tipo_atendimento="Consulta",
        )
        self.atendimento_url = reverse(
            "atendimento-detail", kwargs={"pk": self.atendimento.pk}
        )

    def test_concluir_atendimento(self):
        # Teste para concluir um atendimento
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("atendimento-concluir", kwargs={"pk": self.atendimento.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.atendimento.refresh_from_db()
        self.assertEqual(self.atendimento.status, "Concluído")

    def test_concluir_atendimento_permissao_negada(self):
        # Teste para garantir que outro profissional não possa concluir o
        # atendimento
        self.client.force_authenticate(user=self.outro_profissional)
        response = self.client.post(
            reverse("atendimento-concluir", kwargs={"pk": self.atendimento.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cancelar_atendimento(self):
        # Teste para cancelar um atendimento
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("atendimento-cancelar", kwargs={"pk": self.atendimento.pk}),
            {"motivo_cancelamento": "Imprevisto"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.atendimento.refresh_from_db()
        self.assertEqual(self.atendimento.status, "Cancelado")

    def test_reagendar_atendimento(self):
        # Teste para reagendar um atendimento
        self.client.force_authenticate(user=self.user_profissional)
        nova_data = timezone.now().date() + timezone.timedelta(days=2)
        response = self.client.post(
            reverse("atendimento-reagendar", kwargs={"pk": self.atendimento.pk}),
            {
                "data_atendimento": nova_data,
                "horario_inicio": "11:00",
                "horario_fim": "12:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.atendimento.refresh_from_db()
        self.assertEqual(self.atendimento.data_atendimento, nova_data)
        self.assertEqual(self.atendimento.horario_inicio, "11:00")
        self.assertEqual(self.atendimento.horario_fim, "12:00")

    def test_meus_atendimentos_paciente(self):
        # Teste para listar atendimentos do paciente autenticado
        self.client.force_authenticate(user=self.user_paciente)
        response = self.client.get(reverse("atendimento-meus-atendimentos"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.atendimento.id)

    def test_meus_atendimentos_profissional(self):
        # Teste para listar atendimentos do profissional autenticado
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.get(reverse("atendimento-meus-atendimentos"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.atendimento.id)

    def test_notificacao_concluir_atendimento(self, mock_send_notification):
        # Teste para garantir que a notificação é enviada ao concluir o
        # atendimento
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("atendimento-concluir", kwargs={"pk": self.atendimento.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_notification.assert_called_once()
