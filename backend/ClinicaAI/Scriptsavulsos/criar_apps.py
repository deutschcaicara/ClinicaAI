import os

BASE_DIR = "/mnt/dados/ClinicaAI/backend/apps"  # Caminho base para seus apps
apps = [
    'whatsapp', 'conhecimento', 'voip', 'iot', 'aprovacoes', 'mensagens', 'produtividade', 
    'compromissos', 'central_ajuda', 'servico_campo', 'planilhas_horas', 'projeto', 'pesquisas',
    'automacao_marketing', 'eventos', 'marketing_sms', 'marketing_email', 'redes_sociais', 
    'frota', 'indicacoes', 'avaliacoes', 'folgas', 'recrutamento', 'recursos_humanos', 'qualidade',
    'manutencao', 'compras', 'plm', 'fabricacao', 'inventario', 'elearning', 'chat_ao_vivo',
    'forum', 'blog', 'ecommerce', 'criador_sites', 'locacao', 'assinaturas', 'crm', 'vendas',
    'assinar_documentos', 'documentos', 'planilhas', 'despesas', 'faturamento', 'financeiro',
    'agendamentos', 'pacientes'
]

for app in apps:
    app_dir = os.path.join(BASE_DIR, app)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
        # Criando arquivos básicos em cada app
        with open(os.path.join(app_dir, 'models.py'), 'w') as f:
            f.write(f"from django.db import models\n\n"
                    f"class {app.capitalize()}(models.Model):\n"
                    f"    nome = models.CharField(max_length=100)\n\n"
                    f"    def __str__(self):\n"
                    f"        return self.nome\n")

        with open(os.path.join(app_dir, 'views.py'), 'w') as f:
            f.write(f"from rest_framework import viewsets\n"
                    f"from .models import {app.capitalize()}\n"
                    f"from .serializers import {app.capitalize()}Serializer\n\n"
                    f"class {app.capitalize()}ViewSet(viewsets.ModelViewSet):\n"
                    f"    queryset = {app.capitalize()}.objects.all()\n"
                    f"    serializer_class = {app.capitalize()}Serializer\n")

        with open(os.path.join(app_dir, 'serializers.py'), 'w') as f:
            f.write(f"from rest_framework import serializers\n"
                    f"from .models import {app.capitalize()}\n\n"
                    f"class {app.capitalize()}Serializer(serializers.ModelSerializer):\n"
                    f"    class Meta:\n"
                    f"        model = {app.capitalize()}\n"
                    f"        fields = '__all__'\n")

        with open(os.path.join(app_dir, 'admin.py'), 'w') as f:
            f.write(f"from django.contrib import admin\n"
                    f"from .models import {app.capitalize()}\n\n"
                    f"admin.site.register({app.capitalize()})\n")

        with open(os.path.join(app_dir, 'apps.py'), 'w') as f:
            f.write(f"from django.apps import AppConfig\n\n"
                    f"class {app.capitalize()}Config(AppConfig):\n"
                    f"    default_auto_field = 'django.db.models.BigAutoField'\n"
                    f"    name = 'apps.{app}'\n")

print("Estrutura básica dos módulos criada com sucesso.")
