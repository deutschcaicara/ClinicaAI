from django.db import models
from django.utils import timezone
import uuid
from apps.pacientes.models import Paciente

from apps.profissionais.models import Profissional
from django.core.validators import FileExtensionValidator
from django.conf import settings
import hashlib
from datetime import timedelta


class Documento(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    titulo = models.CharField(max_length=255, verbose_name="Título do Documento")
    descricao = models.TextField(
        verbose_name="Descrição do Documento", blank=True, null=True
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(
        Profissional,
        on_delete=models.SET_NULL,
        null=True,
        related_name="documentos_criados",
    )
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="documentos",
        blank=True,
        null=True,
    )
    arquivo = models.FileField(
        upload_to="documentos/",
        verbose_name="Arquivo do Documento",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    status = models.CharField(
        max_length=20,
        choices=[("Pendente", "Pendente"), ("Assinado", "Assinado")],
        default="Pendente",
    )
    data_expiracao = models.DateField(
        blank=True, null=True, verbose_name="Data de Expiração do Documento"
    )
    hash_documento = models.CharField(
        max_length=256, verbose_name="Hash do Documento", blank=True, null=True
    )
    consentimento_informado = models.BooleanField(
        default=False, verbose_name="Consentimento Informado"
    )
    exigencias_legais = models.TextField(
        verbose_name="Exigências Legais", blank=True, null=True
    )
    versao = models.IntegerField(default=1, verbose_name="Versão do Documento")
    compliance_regulamentar = models.TextField(
        verbose_name="Conformidade Regulamentar", blank=True, null=True
    )
    associado_prontuario = models.BooleanField(
        default=False, verbose_name="Associado ao Prontuário"
    )
    analise_automatizada = models.TextField(
        verbose_name="Análise Automatizada de Risco", blank=True, null=True
    )

    class Meta:
        ordering = ["-data_criacao"]
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"

    def is_expired(self):
        # Verifica se o documento está expirado
        if self.data_expiracao:
            return timezone.now().date() > self.data_expiracao
        return False

    def gerar_hash_documento(self):
        # Gera o hash do documento para garantir integridade
        if self.arquivo:
            hasher = hashlib.sha256()
            with self.arquivo.open("rb") as f:
                buf = f.read()
                hasher.update(buf)
            self.hash_documento = hasher.hexdigest()
            self.save()

    def definir_expiracao_padrao(self):
        # Define uma data de expiração padrão para o documento se não estiver
        # definida
        if not self.data_expiracao:
            self.data_expiracao = timezone.now().date() + timedelta(days=365)
            self.save()


class Assinatura(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    documento = models.ForeignKey(
        Documento, on_delete=models.CASCADE, related_name="assinaturas"
    )
    assinante = models.ForeignKey(
        Profissional, on_delete=models.CASCADE, related_name="assinaturas_realizadas"
    )
    data_assinatura = models.DateTimeField(default=timezone.now)
    assinatura_eletronica = models.TextField(
        verbose_name="Assinatura Eletrônica", blank=True, null=True
    )
    validade_assinatura = models.DateField(
        blank=True, null=True, verbose_name="Validade da Assinatura"
    )
    ip_assinatura = models.GenericIPAddressField(
        verbose_name="Endereço IP da Assinatura", blank=True, null=True
    )
    localizacao_assinatura = models.CharField(
        max_length=255, verbose_name="Localização da Assinatura", blank=True, null=True
    )
    biometria_hash = models.CharField(
        max_length=256, verbose_name="Hash da Biometria", blank=True, null=True
    )
    dupla_autenticacao = models.BooleanField(
        default=False, verbose_name="Autenticação em Duas Etapas"
    )
    ferramenta_dispositivo = models.CharField(
        max_length=100,
        verbose_name="Ferramenta/Dispositivo Utilizado",
        blank=True,
        null=True,
    )
    historico_eventos = models.TextField(
        verbose_name="Histórico de Eventos", blank=True, null=True
    )

    class Meta:
        ordering = ["-data_assinatura"]
        verbose_name = "Assinatura"
        verbose_name_plural = "Assinaturas"

    def __str__(self):
        return f"Assinatura de {self.assinante.nome_completo} no documento {self.documento.titulo}"

    def is_valid(self):
        # Verifica se a assinatura ainda é válida
        if self.validade_assinatura:
            return timezone.now().date() <= self.validade_assinatura
        return True

    def gerar_assinatura_eletronica(self):
        # Gera uma assinatura eletrônica única usando hash do documento,
        # informações do assinante e autenticação em duas etapas
        if self.documento and self.assinante:
            dados = f"{self.documento.hash_documento}{self.assinante.uuid}{self.data_assinatura}"
            if self.dupla_autenticacao:
                dados += "dupla_autenticacao"
            self.assinatura_eletronica = hashlib.sha256(dados.encode()).hexdigest()
            self.save()

    def validar_biometria(self, biometria_dados):
        # Valida a biometria fornecida comparando com o hash armazenado
        if biometria_dados:
            biometria_hash = hashlib.sha256(biometria_dados.encode()).hexdigest()
            return biometria_hash == self.biometria_hash
        return False

    def registrar_evento(self, evento):
        # Registra um evento no histórico de assinatura
        if self.historico_eventos:
            self.historico_eventos += f"\n{timezone.now()}: {evento}"
        else:
            self.historico_eventos = f"{timezone.now()}: {evento}"
        self.save()
