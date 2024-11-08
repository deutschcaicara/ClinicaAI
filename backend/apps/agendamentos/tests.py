# Módulo Agendamentos - Tests (tests.py)

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Agendamento
from apps.pacientes.models import Paciente
from apps.profissionais.models import Profissional
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid
from unittest.mock import patch

User = get_user_model()

class AgendamentoAPITestCase(APITestCase):
    def setUp(self):
        # Configurar usuários, paciente, profissional e agendamento para os testes
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

        self.user_outro_paciente = User.objects.create_user(
            username="outro_paciente", password="testpassword"
        )
        self.outro_paciente = Paciente.objects.create(
            usuario=self.user_outro_paciente, nome_completo="Outro Paciente Teste"
        )

        self.agendamento = Agendamento.objects.create(
            uuid=uuid.uuid4(),
            paciente=self.paciente,
            profissional=self.profissional,
            data_agendamento=timezone.now().date() + timezone.timedelta(days=1),
            horario_inicio="10:00",
            horario_fim="11:00",
            tipo_consulta="Consulta Inicial",
        )
        self.agendamento_url = reverse(
            "agendamento-detail", kwargs={"pk": self.agendamento.pk}
        )

    def test_confirmar_agendamento(self):
        # Teste para confirmar um agendamento
        self.client.force_authenticate(user=self.user_paciente)
        response = self.client.post(
            reverse("agendamento-confirmar", kwargs={"pk": self.agendamento.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.agendamento.refresh_from_db()
        self.assertTrue(self.agendamento.confirmado_pelo_paciente)

    def test_confirmar_agendamento_outro_paciente(self):
        # Teste para garantir que um paciente não possa confirmar agendamento de outro paciente
        self.client.force_authenticate(user=self.user_outro_paciente)
        response = self.client.post(
            reverse("agendamento-confirmar", kwargs={"pk": self.agendamento.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cancelar_agendamento(self):
        # Teste para cancelar um agendamento
        self.client.force_authenticate(user=self.user_paciente)
        response = self.client.post(
            reverse("agendamento-cancelar", kwargs={"pk": self.agendamento.pk}),
            {"motivo_cancelamento": "Imprevisto"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, "Cancelado")
        self.assertEqual(self.agendamento.motivo_cancelamento, "Imprevisto")

    def test_cancelar_agendamento_outro_paciente(self):
        # Teste para garantir que um paciente não possa cancelar agendamento de outro paciente
        self.client.force_authenticate(user=self.user_outro_paciente)
        response = self.client.post(
            reverse("agendamento-cancelar", kwargs={"pk": self.agendamento.pk}),
            {"motivo_cancelamento": "Imprevisto"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reagendar_agendamento(self):
        # Teste para reagendar um agendamento
        self.client.force_authenticate(user=self.user_paciente)
        nova_data = timezone.now().date() + timezone.timedelta(days=2)
        response = self.client.post(
            reverse("agendamento-reagendar", kwargs={"pk": self.agendamento.pk}),
            {
                "data_agendamento": nova_data,
                "horario_inicio": "11:00",
                "horario_fim": "12:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.data_agendamento, nova_data)
        self.assertEqual(self.agendamento.horario_inicio, "11:00")
        self.assertEqual(self.agendamento.horario_fim, "12:00")

    def test_reagendar_agendamento_data_passada(self):
        # Teste para garantir que não seja possível reagendar para uma data passada
        self.client.force_authenticate(user=self.user_paciente)
        nova_data = timezone.now().date() - timezone.timedelta(days=1)
        response = self.client.post(
            reverse("agendamento-reagendar", kwargs={"pk": self.agendamento.pk}),
            {
                "data_agendamento": nova_data,
                "horario_inicio": "11:00",
                "horario_fim": "12:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("apps.agendamentos.views.send_notification")
    def test_confirmar_agendamento_notificacao(self, mock_send_notification):
        # Teste para confirmar um agendamento e verificar se a notificação foi enviada
        self.client.force_authenticate(user=self.user_paciente)
        response = self.client.post(
            reverse("agendamento-confirmar", kwargs={"pk": self.agendamento.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_notification.assert_called_once()

    def test_meus_agendamentos(self):
        # Teste para listar agendamentos do paciente autenticado
        self.client.force_authenticate(user=self.user_paciente)
        response = self.client.get(reverse("agendamento-meus-agendamentos"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.agendamento.id)

    def test_meus_agendamentos_outro_paciente(self):
        # Teste para garantir que um paciente veja apenas seus próprios agendamentos
        self.client.force_authenticate(user=self.user_outro_paciente)
        response = self.client.get(reverse("agendamento-meus-agendamentos"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
