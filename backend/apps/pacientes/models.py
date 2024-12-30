from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import timezone

# Gerar uma chave de criptografia para uso nos campos sensíveis (a chave deve ser armazenada em um local seguro)
# Aqui estamos simulando a recuperação da chave do arquivo de configurações
cipher_suite = Fernet(settings.ENCRYPTION_KEY)


class Paciente(models.Model):
    # Identificador Único Global
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)


    # Dados Pessoais
    nome_completo = models.CharField(_("Nome Completo"), max_length=255)
    foto = models.ImageField(
        _("Foto"), upload_to="pacientes/fotos/", blank=True, null=True
    )
    cpf = models.CharField(_("CPF"), max_length=255, unique=True)
    rg = models.CharField(_("RG"), max_length=255, blank=True)
    data_nascimento = models.DateField(_("Data de Nascimento"))
    sexo = models.CharField(
        _("Sexo"),
        max_length=1,
        choices=[
            ("M", "Masculino"),
            ("F", "Feminino"),
            ("O", "Outro"),
        ],
    )
    estado_civil = models.CharField(_("Estado Civil"), max_length=50, blank=True)
    profissao = models.CharField(_("Profissão"), max_length=100, blank=True)
    nacionalidade = models.CharField(_("Nacionalidade"), max_length=100, blank=True)
    naturalidade = models.CharField(_("Naturalidade"), max_length=100, blank=True)
    endereco = models.CharField(_("Endereço"), max_length=255)
    numero = models.CharField(_("Número"), max_length=10)
    complemento = models.CharField(_("Complemento"), max_length=100, blank=True)
    bairro = models.CharField(_("Bairro"), max_length=100)
    cidade = models.CharField(_("Cidade"), max_length=100)
    estado = models.CharField(_("Estado"), max_length=100)
    cep = models.CharField(_("CEP"), max_length=9, blank=True)
    telefone_residencial = models.CharField(
        _("Telefone Residencial"), max_length=20, blank=True
    )
    telefone_celular = models.CharField(
        _("Telefone Celular"), max_length=20, blank=True
    )
    email = models.EmailField(_("E-mail"), blank=True)
    contato_emergencia = models.CharField(
        _("Contato de Emergência"), max_length=255, blank=True
    )
    telefone_emergencia = models.CharField(
        _("Telefone de Emergência"), max_length=20, blank=True
    )

    # Dados Complementares
    nome_mae = models.CharField(_("Nome da Mãe"), max_length=255, blank=True)
    nome_pai = models.CharField(_("Nome do Pai"), max_length=255, blank=True)
    consentimento_lgpd = models.BooleanField(_("Consentimento LGPD"), default=False)
    observacoes = models.TextField(_("Observações"), blank=True)

    # Relacionamentos
    prontuario = models.OneToOneField(
    "prontuarios.Prontuario",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="paciente_prontuario",  
)

    

    # Auditoria
    created_at = models.DateTimeField(_("Data de Criação"), default=timezone.now)

    updated_at = models.DateTimeField(_("Última Atualização"), auto_now=True)

    class Meta:
        app_label = "pacientes"
        verbose_name = _("Paciente")
        verbose_name_plural = _("Pacientes")

    def __str__(self):
        return self.nome_completo

    def save(self, *args, **kwargs):
        # Criptografar CPF e RG antes de salvar
        if self.cpf:
            self.cpf = cipher_suite.encrypt(self.cpf.encode()).decode()
        if self.rg:
            self.rg = cipher_suite.encrypt(self.rg.encode()).decode()
        super().save(*args, **kwargs)

    def decrypt_cpf(self):
        # Descriptografar o CPF para uso
        if self.cpf:
            return cipher_suite.decrypt(self.cpf.encode()).decode()
        return None

    def decrypt_rg(self):
        # Descriptografar o RG para uso
        if self.rg:
            return cipher_suite.decrypt(self.rg.encode()).decode()
        return None
