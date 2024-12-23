# Módulo Exames - Tests (tests.py)

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Exame
from apps.pacientes.models import Paciente
from apps.profissionais.models import Profissional
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
from unittest.mock import patch

User = get_user_model()

User = get_user_model()


class ExameAPITestCase(APITestCase):
    def setUp(self):
        # Configurar usuários, paciente, profissional e exame para os testes
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

        self.exame = Exame.objects.create(
            uuid=uuid.uuid4(),
            paciente=self.paciente,
            profissional_solicitante=self.profissional,
            tipo_exame="Hemograma",
            data_solicitacao=timezone.now().date(),
        )
        self.exame_url = reverse("exame-detail", kwargs={"pk": self.exame.pk})

    def test_registrar_resultado_exame(self):
        # Teste para registrar o resultado de um exame
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("exame-registrar-resultado", kwargs={"pk": self.exame.pk}),
            {
                "resultados": "Resultados normais",
                "status": "Realizado",
                "data_realizacao": timezone.now().date(),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.exame.refresh_from_db()
        self.assertEqual(self.exame.status, "Realizado")
        self.assertEqual(self.exame.resultados, "Resultados normais")

    def test_registrar_resultado_permissao_negada(self):
        # Teste para garantir que outro profissional não possa registrar o
        # resultado do exame
        self.client.force_authenticate(user=self.outro_profissional)
        response = self.client.post(
            reverse("exame-registrar-resultado", kwargs={"pk": self.exame.pk}),
            {"resultados": "Resultados alterados", "status": "Realizado"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cancelar_exame(self):
        # Teste para cancelar um exame
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("exame-cancelar-exame", kwargs={"pk": self.exame.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.exame.refresh_from_db()
        self.assertEqual(self.exame.status, "Cancelado")

    def test_cancelar_exame_por_paciente(self):
        # Teste para garantir que o paciente não possa cancelar o exame
        self.client.force_authenticate(user=self.user_paciente)
        response = self.client.post(
            reverse("exame-cancelar-exame", kwargs={"pk": self.exame.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_registrar_resultado_sem_data_realizacao(self):
        # Teste para tentar registrar o resultado sem fornecer a data de
        # realização
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("exame-registrar-resultado", kwargs={"pk": self.exame.pk}),
            {"resultados": "Resultados normais", "status": "Realizado"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_meus_exames_paciente(self):
        # Teste para listar exames do paciente autenticado
        self.client.force_authenticate(user=self.user_paciente)
        response = self.client.get(reverse("exame-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.exame.id)

    def test_meus_exames_profissional(self):
        # Teste para listar exames solicitados pelo profissional autenticado
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.get(reverse("exame-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.exame.id)

    def test_notificacao_registrar_resultado(self, mock_send_notification):
        # Teste para garantir que a notificação é enviada ao registrar o
        # resultado do exame
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("exame-registrar-resultado", kwargs={"pk": self.exame.pk}),
            {
                "resultados": "Resultados normais",
                "status": "Realizado",
                "data_realizacao": timezone.now().date(),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_notification.assert_called_once()

    def test_notificacao_cancelar_exame(self, mock_send_notification):
        # Teste para garantir que a notificação é enviada ao cancelar um exame
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("exame-cancelar-exame", kwargs={"pk": self.exame.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_notification.assert_called_once()

    @patch("exames.views.ExameViewSet.analisar_resultados")
    def test_integracao_machine_learning(self, mock_analisar_resultados):
        # Teste para garantir que a integração com Machine Learning seja
        # acionada ao registrar resultados
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("exame-registrar-resultado", kwargs={"pk": self.exame.pk}),
            {
                "resultados": "Resultados normais",
                "status": "Realizado",
                "data_realizacao": timezone.now().date(),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_analisar_resultados.assert_called_once_with(self.exame)
