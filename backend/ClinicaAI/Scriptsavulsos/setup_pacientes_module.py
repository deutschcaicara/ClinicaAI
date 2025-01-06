import os
import subprocess

BASE_DIR = "/mnt/dados/ClinicaAI/backend/apps/pacientes"

def criar_pasta_se_necessario():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
        print(f"Pasta {BASE_DIR} criada com sucesso.")

def criar_models():
    models_path = os.path.join(BASE_DIR, 'models.py')
    with open(models_path, 'w') as f:
        f.write("""
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
""")
    print("Arquivo models.py criado com sucesso.")

def criar_serializers():
    serializers_path = os.path.join(BASE_DIR, 'serializers.py')
    with open(serializers_path, 'w') as f:
        f.write("""
from rest_framework import serializers
from .models import Paciente

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'
""")
    print("Arquivo serializers.py criado com sucesso.")

def criar_views():
    views_path = os.path.join(BASE_DIR, 'views.py')
    with open(views_path, 'w') as f:
        f.write("""
from rest_framework import viewsets
from .models import Paciente
from .serializers import PacienteSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
""")
    print("Arquivo views.py criado com sucesso.")

def criar_urls():
    urls_path = os.path.join(BASE_DIR, 'urls.py')
    with open(urls_path, 'w') as f:
        f.write("""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PacienteViewSet

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
""")
    print("Arquivo urls.py criado com sucesso.")

def criar_admin():
    admin_path = os.path.join(BASE_DIR, 'admin.py')
    with open(admin_path, 'w') as f:
        f.write("""
from django.contrib import admin
from .models import Paciente

admin.site.register(Paciente)
""")
    print("Arquivo admin.py criado com sucesso.")

def rodar_migracoes():
    # Executar os comandos de makemigrations e migrate
    try:
        subprocess.run(["python", "manage.py", "makemigrations", "pacientes"], check=True)
        subprocess.run(["python", "manage.py", "migrate"], check=True)
        print("Migrações criadas e aplicadas com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao rodar migrações: {e}")

if __name__ == "__main__":
    criar_pasta_se_necessario()
    criar_models()
    criar_serializers()
    criar_views()
    criar_urls()
    criar_admin()
    rodar_migracoes()
