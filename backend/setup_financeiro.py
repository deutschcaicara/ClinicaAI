import os
import concurrent.futures
from django.core.management import call_command
import django


def criar_estrutura_modulo(modulo_nome, base_path):
    pasta_modulo = os.path.join(base_path, "apps", modulo_nome)

    try:
        # Criar pasta do módulo
        os.makedirs(pasta_modulo, exist_ok=True)
        print(f"Pasta {pasta_modulo} criada com sucesso.")

        # Criar models.py
        models_content = f"""from django.db import models

class {modulo_nome.capitalize()}Model(models.Model):
    nome = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
"""
        criar_arquivo(os.path.join(pasta_modulo, "models.py"), models_content)

        # Criar serializers.py
        serializers_content = f"""from rest_framework import serializers
from .models import {modulo_nome.capitalize()}Model

class {modulo_nome.capitalize()}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {modulo_nome.capitalize()}Model
        fields = '__all__'
"""
        criar_arquivo(os.path.join(pasta_modulo, "serializers.py"), serializers_content)

        # Criar views.py
        views_content = f"""from rest_framework import viewsets
from .models import {modulo_nome.capitalize()}Model
from .serializers import {modulo_nome.capitalize()}Serializer

class {modulo_nome.capitalize()}ViewSet(viewsets.ModelViewSet):
    queryset = {modulo_nome.capitalize()}Model.objects.all()
    serializer_class = {modulo_nome.capitalize()}Serializer
"""
        criar_arquivo(os.path.join(pasta_modulo, "views.py"), views_content)

        # Criar urls.py
        urls_content = f"""from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import {modulo_nome.capitalize()}ViewSet

router = DefaultRouter()
router.register(r'{modulo_nome}', {modulo_nome.capitalize()}ViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
"""
        criar_arquivo(os.path.join(pasta_modulo, "urls.py"), urls_content)

        # Criar admin.py
        admin_content = f"""from django.contrib import admin
from .models import {modulo_nome.capitalize()}Model

@admin.register({modulo_nome.capitalize()}Model)
class {modulo_nome.capitalize()}Admin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
"""
        criar_arquivo(os.path.join(pasta_modulo, "admin.py"), admin_content)

        print(f"Arquivos do módulo {modulo_nome} criados com sucesso.")

    except Exception as e:
        print(f"Erro ao criar estrutura do módulo {modulo_nome}: {e}")


def criar_estrutura_modulos(base_path):
    settings_path = os.path.join(base_path, "ClinicaAI", "settings.py")
    modulos = [
        "crm",
        "vendas",
        "recrutamento",
        "recursos_humanos",
        "ecommerce",
        "compromissos",
        "mensagens",
        "servico_campo",
        "planilhas_horas",
        "projeto",
        "qualidade",
        "compras",
        "manutencao",
        "forum",
        "blog",
        "elearning",
        "plm",
        "fabricacao",
        "inventario",
        "chat_ao_vivo",
        "criador_sites",
        "locacao",
        "assinaturas",
        "assinar_documentos",
        "documentos",
        "planilhas",
        "despesas",
        "faturamento",
        "marketing_sms",
        "marketing_email",
        "redes_sociais",
        "frota",
        "indicacoes",
        "avaliacoes",
        "folgas",
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda modulo: criar_estrutura_modulo(modulo, base_path), modulos)

    # Atualizar urls.py principal
    urls_principal_path = os.path.join(base_path, "ClinicaAI", "urls.py")
    urls_principal_content = [
        "from django.contrib import admin",
        "from django.urls import path, include",
        "",
        "urlpatterns = [",
        "    path('admin/', admin.site.urls),",
    ]
    for modulo_nome in modulos:
        urls_principal_content.append(
            f"    path('{modulo_nome}/', include('apps.{modulo_nome}.urls')),"
        )
    urls_principal_content.append("]")
    urls_principal_content = "\n".join(urls_principal_content)
    criar_arquivo(urls_principal_path, urls_principal_content)

    # Atualizar settings.py para incluir os módulos em INSTALLED_APPS
    atualizar_installed_apps(settings_path, modulos)


def atualizar_installed_apps(settings_path, modulos):
    with open(settings_path, "r") as settings_file:
        settings_content = settings_file.read()

    installed_apps_start = settings_content.find("INSTALLED_APPS = [")
    if installed_apps_start != -1:
        installed_apps_end = settings_content.find("\n]", installed_apps_start) + 1
        installed_apps_section = settings_content[
            installed_apps_start:installed_apps_end
        ]
        for modulo_nome in modulos:
            app_entry = f"    'apps.{modulo_nome}',"
            if app_entry not in installed_apps_section:
                installed_apps_section += f"\n{app_entry}"
        new_settings_content = (
            settings_content[:installed_apps_start]
            + installed_apps_section
            + settings_content[installed_apps_end:]
        )
        criar_arquivo(settings_path, new_settings_content)


def criar_arquivo(caminho, conteudo):
    with open(caminho, "w") as arquivo:
        arquivo.write(conteudo)
    print(f"Arquivo {caminho} criado com sucesso.")


if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    criar_estrutura_modulos(base_path)

    # Configurar as configurações do Django antes de rodar os comandos de migração
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ClinicaAI.settings")
    django.setup()

    # Após criar os arquivos, rodar as migrações para todos os módulos
    call_command("makemigrations")
    call_command("migrate")
