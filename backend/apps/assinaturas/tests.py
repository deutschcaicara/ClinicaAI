# Módulo Assinaturas - Tests (tests.py)

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Documento, Assinatura
from apps.pacientes.models import Paciente

from apps.profissionais.models import Profissional

from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
from unittest.mock import patch

User = get_user_model()


class AssinaturasAPITestCase(APITestCase):
    def setUp(self):
        # Configurar usuários, paciente, profissional, documento e assinatura
        # para os testes
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

        self.documento = Documento.objects.create(
            uuid=uuid.uuid4(),
            titulo="Documento Teste",
            descricao="Descrição do documento teste",
            autor=self.profissional,
            paciente=self.paciente,
            data_expiracao=timezone.now().date() + timezone.timedelta(days=30),
            status="Pendente",
        )
        self.documento_url = reverse(
            "documento-detail", kwargs={"pk": self.documento.pk}
        )

    def test_assinar_documento(self):
        # Teste para assinar um documento
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("documento-assinar", kwargs={"pk": self.documento.pk}),
            {
                "dupla_autenticacao": True,
                "biometria_hash": "hash_teste",
                "localizacao_assinatura": "Local Teste",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.documento.refresh_from_db()
        self.assertEqual(self.documento.status, "Assinado")

    def test_assinar_documento_expirado(self):
        # Teste para garantir que não é possível assinar um documento expirado
        self.documento.data_expiracao = timezone.now().date() - timezone.timedelta(
            days=1
        )
        self.documento.save()
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("documento-assinar", kwargs={"pk": self.documento.pk}),
            {
                "dupla_autenticacao": True,
                "biometria_hash": "hash_teste",
                "localizacao_assinatura": "Local Teste",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Não é possível assinar um documento expirado.", response.data["detail"]
        )

    def test_cancelar_assinatura(self):
        # Teste para cancelar uma assinatura
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("documento-assinar", kwargs={"pk": self.documento.pk}),
            {
                "dupla_autenticacao": True,
                "biometria_hash": "hash_teste",
                "localizacao_assinatura": "Local Teste",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assinatura = Assinatura.objects.get(documento=self.documento)

        response = self.client.post(
            reverse("assinatura-cancelar-assinatura", kwargs={"pk": assinatura.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Assinatura.objects.filter(pk=assinatura.pk).exists())
        self.documento.refresh_from_db()
        self.assertEqual(self.documento.status, "Pendente")

    def test_validar_assinatura(self):
        # Teste para validar uma assinatura
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("documento-assinar", kwargs={"pk": self.documento.pk}),
            {
                "dupla_autenticacao": True,
                "biometria_hash": "hash_teste",
                "localizacao_assinatura": "Local Teste",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assinatura = Assinatura.objects.get(documento=self.documento)

        response = self.client.post(
            reverse("assinatura-validar-assinatura", kwargs={"pk": assinatura.pk}),
            {"biometria_dados": "hash_teste"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "A assinatura é válida.")

    def test_notificacao_assinatura_documento(self, mock_send_notification):
        # Teste para garantir que a notificação é enviada ao assinar um
        # documento
        self.client.force_authenticate(user=self.user_profissional)
        response = self.client.post(
            reverse("documento-assinar", kwargs={"pk": self.documento.pk}),
            {
                "dupla_autenticacao": True,
                "biometria_hash": "hash_teste",
                "localizacao_assinatura": "Local Teste",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_notification.assert_called_once()
