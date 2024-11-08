import os
import subprocess

BASE_DIR = "/mnt/dados/ClinicaAI/backend/apps"
SETTINGS_FILE = "/mnt/dados/ClinicaAI/backend/ClinicaAI/settings.py"


def adicionar_ao_installed_apps(nome_modulo):
    # Verificar e adicionar o módulo ao INSTALLED_APPS se ainda não estiver lá
    with open(SETTINGS_FILE, "r") as f:
        settings_content = f.readlines()

    installed_apps_index = None
    for i, line in enumerate(settings_content):
        if "INSTALLED_APPS" in line:
            installed_apps_index = i
            break

    if installed_apps_index is not None:
        modulo_entry = f"    'apps.{nome_modulo}',\n"
        if modulo_entry not in settings_content:
            # Adicionar após a linha "INSTALLED_APPS = ["
            settings_content.insert(installed_apps_index + 2, modulo_entry)
            with open(SETTINGS_FILE, "w") as f:
                f.writelines(settings_content)
            print(f"Módulo 'apps.{nome_modulo}' adicionado ao INSTALLED_APPS.")


def criar_pasta_modulo(nome_modulo):
    app_dir = os.path.join(BASE_DIR, nome_modulo)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
        print(f"Pasta {app_dir} criada com sucesso.")
    return app_dir


def criar_models_agendamento(app_dir):
    models_path = os.path.join(app_dir, "models.py")
    with open(models_path, "w") as f:
        f.write(
            """
from django.db import models
from apps.pacientes.models import Paciente

class Agendamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='agendamentos')
    data_horario = models.DateTimeField()
    tipo_consulta = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[
        ('agendado', 'Agendado'),
        ('cancelado', 'Cancelado'),
        ('realizado', 'Realizado'),
    ])
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"Agendamento de {self.paciente.nome_completo} em {self.data_horario}"
"""
        )
    print("Arquivo models.py para Agendamento criado com sucesso.")


def criar_models_prontuario(app_dir):
    models_path = os.path.join(app_dir, "models.py")
    with open(models_path, "w") as f:
        f.write(
            """
from django.db import models
from apps.pacientes.models import Paciente

class Prontuario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='prontuarios')
    data_registro = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    medico_responsavel = models.CharField(max_length=100)

    def __str__(self):
        return f"Prontuário de {self.paciente.nome_completo} - {self.data_registro.strftime('%d/%m/%Y')}"
"""
        )
    print("Arquivo models.py para Prontuário criado com sucesso.")


def criar_views_serializers_urls(nome_modulo):
    app_dir = os.path.join(BASE_DIR, nome_modulo)

    # Nome da classe do modelo no singular
    nome_classe = (
        nome_modulo.capitalize()[:-1]
        if nome_modulo.endswith("s")
        else nome_modulo.capitalize()
    )

    # Criar serializers.py
    serializers_path = os.path.join(app_dir, "serializers.py")
    with open(serializers_path, "w") as f:
        f.write(
            f"""
from rest_framework import serializers
from .models import {nome_classe}

class {nome_classe}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {nome_classe}
        fields = '__all__'
"""
        )
    print(f"Arquivo serializers.py para {nome_classe} criado com sucesso.")

    # Criar views.py
    views_path = os.path.join(app_dir, "views.py")
    with open(views_path, "w") as f:
        f.write(
            f"""
from rest_framework import viewsets
from .models import {nome_classe}
from .serializers import {nome_classe}Serializer

class {nome_classe}ViewSet(viewsets.ModelViewSet):
    queryset = {nome_classe}.objects.all()
    serializer_class = {nome_classe}Serializer
"""
        )
    print(f"Arquivo views.py para {nome_classe} criado com sucesso.")

    # Criar urls.py
    urls_path = os.path.join(app_dir, "urls.py")
    with open(urls_path, "w") as f:
        f.write(
            f"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import {nome_classe}ViewSet

router = DefaultRouter()
router.register(r'{nome_modulo.lower()}', {nome_classe}ViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
"""
        )
    print(f"Arquivo urls.py para {nome_classe} criado com sucesso.")


def criar_admin(nome_modulo):
    app_dir = os.path.join(BASE_DIR, nome_modulo)

    # Nome da classe do modelo no singular
    nome_classe = (
        nome_modulo.capitalize()[:-1]
        if nome_modulo.endswith("s")
        else nome_modulo.capitalize()
    )

    admin_path = os.path.join(app_dir, "admin.py")
    with open(admin_path, "w") as f:
        f.write(
            f"""
from django.contrib import admin
from .models import {nome_classe}

admin.site.register({nome_classe})
"""
        )
    print(f"Arquivo admin.py para {nome_classe} criado com sucesso.")


def rodar_migracoes():
    # Executar os comandos de makemigrations e migrate
    try:
        subprocess.run(["python", "manage.py", "makemigrations"], check=True)
        subprocess.run(["python", "manage.py", "migrate"], check=True)
        print("Migrações criadas e aplicadas com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao rodar migrações: {e}")


if __name__ == "__main__":
    # Criar módulo Agendamentos
    agendamento_dir = criar_pasta_modulo("agendamentos")
    criar_models_agendamento(agendamento_dir)
    criar_views_serializers_urls("agendamentos")
    criar_admin("agendamentos")
    adicionar_ao_installed_apps("agendamentos")

    # Criar módulo Prontuário
    prontuario_dir = criar_pasta_modulo("prontuarios")
    criar_models_prontuario(prontuario_dir)
    criar_views_serializers_urls("prontuarios")
    criar_admin("prontuarios")
    adicionar_ao_installed_apps("prontuarios")

    # Rodar migrações
    rodar_migracoes()
