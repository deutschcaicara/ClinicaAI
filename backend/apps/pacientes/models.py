
from django.db import models
from django.utils.translation import gettext_lazy as _

class Paciente(models.Model):
    # Dados Pessoais
    nome_completo = models.CharField(_("Nome Completo"), max_length=255)
    cpf = models.CharField(_("CPF"), max_length=14, unique=True)
    rg = models.CharField(_("RG"), max_length=20, blank=True)
    data_nascimento = models.DateField(_("Data de Nascimento"))
    sexo = models.CharField(
        _("Sexo"),
        max_length=1,
        choices=[
            ('M', 'Masculino'),
            ('F', 'Feminino'),
            ('O', 'Outro'),
        ]
    )
    estado_civil = models.CharField(_("Estado Civil"), max_length=50, blank=True)
    profissao = models.CharField(_("Profissão"), max_length=100, blank=True)
    endereco = models.CharField(_("Endereço"), max_length=255)
    numero = models.CharField(_("Número"), max_length=10)
    complemento = models.CharField(_("Complemento"), max_length=100, blank=True)
    bairro = models.CharField(_("Bairro"), max_length=100)
    cidade = models.CharField(_("Cidade"), max_length=100)
    estado = models.CharField(_("Estado"), max_length=2)
    cep = models.CharField(_("CEP"), max_length=9)
    telefone_fixo = models.CharField(_("Telefone Fixo"), max_length=15, blank=True)
    telefone_celular = models.CharField(_("Telefone Celular"), max_length=15)
    email = models.EmailField(_("Email"), blank=True)
    convenio = models.CharField(_("Convênio"), max_length=100, blank=True)
    numero_carteirinha = models.CharField(_("Número da Carteirinha"), max_length=50, blank=True)
    validade_carteirinha = models.DateField(_("Validade da Carteirinha"), blank=True, null=True)
    responsavel_financeiro = models.CharField(_("Responsável Financeiro"), max_length=255, blank=True)
    parentesco_responsavel = models.CharField(_("Parentesco do Responsável"), max_length=50, blank=True)
    cpf_responsavel = models.CharField(_("CPF do Responsável"), max_length=14, blank=True)
    rg_responsavel = models.CharField(_("RG do Responsável"), max_length=20, blank=True)
    telefone_responsavel = models.CharField(_("Telefone do Responsável"), max_length=15, blank=True)
    consentimento_lgpd = models.BooleanField(_("Consentimento LGPD"), default=False)
    data_consentimento = models.DateTimeField(_("Data do Consentimento"), blank=True, null=True)
    observacoes = models.TextField(_("Observações"), blank=True)
    foto = models.ImageField(_("Foto"), upload_to='fotos_pacientes', blank=True)
    data_cadastro = models.DateTimeField(_("Data do Cadastro"), auto_now_add=True)
    data_atualizacao = models.DateTimeField(_("Data da Última Atualização"), auto_now=True)

    def __str__(self):
        return self.nome_completo

    class Meta:
        verbose_name = _("Paciente")
        verbose_name_plural = _("Pacientes")
