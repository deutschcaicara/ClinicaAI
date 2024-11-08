import os

BASE_DIR = "/mnt/dados/ClinicaAI/backend/apps"  # Caminho base para seus apps

# Lista de todos os aplicativos que criamos
apps = [
    "whatsapp",
    "conhecimento",
    "voip",
    "iot",
    "aprovacoes",
    "mensagens",
    "produtividade",
    "compromissos",
    "central_ajuda",
    "servico_campo",
    "planilhas_horas",
    "projeto",
    "pesquisas",
    "automacao_marketing",
    "eventos",
    "marketing_sms",
    "marketing_email",
    "redes_sociais",
    "frota",
    "indicacoes",
    "avaliacoes",
    "folgas",
    "recrutamento",
    "recursos_humanos",
    "qualidade",
    "manutencao",
    "compras",
    "plm",
    "fabricacao",
    "inventario",
    "elearning",
    "chat_ao_vivo",
    "forum",
    "blog",
    "ecommerce",
    "criador_sites",
    "locacao",
    "assinaturas",
    "crm",
    "vendas",
    "assinar_documentos",
    "documentos",
    "planilhas",
    "despesas",
    "faturamento",
    "financeiro",
    "agendamentos",
    "pacientes",
]

# Corrigir o arquivo apps.py de cada módulo
for app in apps:
    app_dir = os.path.join(BASE_DIR, app)
    apps_file_path = os.path.join(app_dir, "apps.py")

    # Verificar se o arquivo apps.py existe
    if os.path.exists(apps_file_path):
        # Reescrever o arquivo apps.py com o valor correto para name
        with open(apps_file_path, "w") as f:
            f.write(
                f"from django.apps import AppConfig\n\n"
                f"class {app.capitalize()}Config(AppConfig):\n"
                f"    default_auto_field = 'django.db.models.BigAutoField'\n"
                f"    name = 'apps.{app}'\n"
            )

print("Correção dos arquivos apps.py concluída com sucesso.")
