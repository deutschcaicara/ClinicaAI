#!/bin/bash

# Definir variáveis importantes
PROJECT_ROOT="/mnt/dados/ClinicaAI"
APPS_DIR="$PROJECT_ROOT/backend/apps"
VENV_DIR="$PROJECT_ROOT/env"
SETTINGS_FILE="$PROJECT_ROOT/backend/ClinicaAI/settings.py"

# Navegar até a pasta de apps do projeto
cd $APPS_DIR

# Criar novos diretórios para os módulos se ainda não existirem
for module in profissionais atendimentos exames prontuarios; do
  if [ ! -d "$module" ]; then
    mkdir -p $module
  fi

  # Criar __init__.py se ainda não existir
  if [ ! -f "$module/__init__.py" ]; then
    touch $module/__init__.py
  fi

  # Criar models.py se ainda não existir
  if [ ! -f "$module/models.py" ]; then
    case $module in
      profissionais)
        cat <<EOF > $module/models.py
from django.db import models

class ProfissionalSaude(models.Model):
    nome_completo = models.CharField(max_length=255)
    especialidade = models.CharField(max_length=100)
    registro_profissional = models.CharField(max_length=50)
    contato = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.nome_completo} - {self.especialidade}"
EOF
        ;;
      prontuarios)
        cat <<EOF > $module/models.py
from django.db import models
from apps.pacientes.models import Paciente
from apps.profissionais.models import ProfissionalSaude
import datetime

class Prontuario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='prontuarios')
    data_criacao = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prontuário de {self.paciente.nome_completo}"
EOF
        ;;
      atendimentos)
        cat <<EOF > $module/models.py
from django.db import models
from apps.prontuarios.models import Prontuario
from apps.profissionais.models import ProfissionalSaude

class Atendimento(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='atendimentos')
    profissional = models.ForeignKey(ProfissionalSaude, on_delete=models.SET_NULL, null=True, related_name='atendimentos')
    data_atendimento = models.DateTimeField()
    tipo_atendimento = models.CharField(max_length=100, choices=[
        ('consulta', 'Consulta'),
        ('emergencia', 'Emergência'),
        ('retorno', 'Retorno'),
    ])
    descricao = models.TextField()
    receita = models.TextField(blank=True)

    def __str__(self):
        return f"Atendimento em {self.data_atendimento.strftime('%d/%m/%Y')} por {self.profissional}"
EOF
        ;;
      exames)
        cat <<EOF > $module/models.py
from django.db import models
from apps.prontuarios.models import Prontuario
from apps.profissionais.models import ProfissionalSaude

class Exame(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='exames')
    tipo_exame = models.CharField(max_length=100)
    data_solicitacao = models.DateTimeField()
    data_resultado = models.DateTimeField(blank=True, null=True)
    resultado = models.TextField(blank=True)
    profissional_solicitante = models.ForeignKey(ProfissionalSaude, on_delete=models.SET_NULL, null=True, related_name='exames_solicitados')

    def __str__(self):
        return f"Exame {self.tipo_exame} solicitado em {self.data_solicitacao.strftime('%d/%m/%Y')}"
EOF
        ;;
    esac
  fi

  # Criar serializers.py se ainda não existir
  if [ ! -f "$module/serializers.py" ]; then
    cat <<EOF > $module/serializers.py
from rest_framework import serializers
from .models import $(echo ${module^} | sed 's/.$//')

class $(echo ${module^} | sed 's/.$//')Serializer(serializers.ModelSerializer):
    class Meta:
        model = $(echo ${module^} | sed 's/.$//')
        fields = '__all__'
EOF
  fi

  # Criar views.py se ainda não existir
  if [ ! -f "$module/views.py" ]; then
    cat <<EOF > $module/views.py
from rest_framework import viewsets
from .models import $(echo ${module^} | sed 's/.$//')
from .serializers import $(echo ${module^} | sed 's/.$//')Serializer

class $(echo ${module^} | sed 's/.$//')ViewSet(viewsets.ModelViewSet):
    queryset = $(echo ${module^} | sed 's/.$//').objects.all()
    serializer_class = $(echo ${module^} | sed 's/.$//')Serializer
EOF
  fi

  # Criar urls.py se ainda não existir
  if [ ! -f "$module/urls.py" ]; then
    cat <<EOF > $module/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import $(echo ${module^} | sed 's/.$//')ViewSet

router = DefaultRouter()
router.register(r'$(echo ${module,,})s', $(echo ${module^} | sed 's/.$//')ViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
EOF
  fi
done

# Migrar as alterações no banco de dados
cd $PROJECT_ROOT/backend

# Atualizar o arquivo de configurações para incluir os novos módulos
modules_to_add=( "profissionais" "atendimentos" "exames" "prontuarios" )
for module in "${modules_to_add[@]}"; do
  if [ -f "$SETTINGS_FILE" ]; then
    if ! grep -q "'apps.$module'" "$SETTINGS_FILE"; then
      sed -i "/INSTALLED_APPS = \[/a \ \ \ \ 'apps.$module'," $SETTINGS_FILE
    fi
  else
    echo "Erro: Arquivo settings.py não encontrado em $SETTINGS_FILE"
    exit 1
  fi
done

# Rodar migrações
if [ -d "$VENV_DIR" ]; then
  source $VENV_DIR/bin/activate
  python manage.py makemigrations --noinput
  python manage.py migrate
  deactivate
else
  echo "Erro: Diretório da virtual environment não encontrado em $VENV_DIR. Certifique-se de que o caminho está correto ou ajuste o script conforme necessário."
  exit 1
fi

# Script para inserir dados básicos nos módulos
cat <<EOF | python manage.py shell
from apps.profissionais.models import ProfissionalSaude
from apps.atendimentos.models import Atendimento
from apps.exames.models import Exame
from apps.prontuarios.models import Prontuario
from apps.pacientes.models import Paciente
import datetime

# Inserir um exemplo de profissional de saúde
profissional = ProfissionalSaude.objects.create(nome_completo='Dr. João da Silva', especialidade='Cardiologia', registro_profissional='CRM12345')

# Inserir um paciente de exemplo
paciente = Paciente.objects.create(nome_completo='Maria Souza', cpf='123.456.789-00', data_nascimento=datetime.date(1990, 5, 14), sexo='F', telefone_celular='(11) 99999-8888')

# Criar um prontuário para o paciente
prontuario = Prontuario.objects.create(paciente=paciente)

# Inserir um exemplo de atendimento
atendimento = Atendimento.objects.create(prontuario=prontuario, profissional=profissional, data_atendimento=datetime.datetime.now(), tipo_atendimento='consulta', descricao='Consulta inicial')

# Inserir um exemplo de exame
exame = Exame.objects.create(prontuario=prontuario, tipo_exame='Eletrocardiograma', data_solicitacao=datetime.datetime.now(), profissional_solicitante=profissional)
EOF
