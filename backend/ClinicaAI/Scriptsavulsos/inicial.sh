#!/bin/bash

# Variáveis de configuração
PROJETO_DIR="/mnt/dados/ClinicaAI"
REPO_GIT="https://github.com/deutschcaicara/ClinicaAI"
DB_USER="diego"
DB_PASSWORD="Mouse2250@#86"

# Atualizando e instalando dependências essenciais
sudo apt update && sudo apt upgrade -y
# Corrigir pacotes quebrados, se houver
sudo apt --fix-broken install -y
if ! sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib git git-lfs docker.io docker-compose nodejs npm curl build-essential libssl-dev libffi-dev python3-dev redis-tools prometheus containerd; then
  echo "Erro ao instalar dependências essenciais. Verifique a conexão e tente novamente."
  exit 1
fi

# Instalar pacotes via Snap
if ! command -v helm &> /dev/null; then
  sudo snap install helm --classic
fi
if ! command -v kubectl &> /dev/null; then
  sudo snap install kubectl --classic
fi
if ! command -v grafana &> /dev/null; then
  sudo snap install grafana
fi

# Verificar se Git LFS está instalado e configurado
if ! git lfs install; then
  echo "Erro ao instalar o Git LFS. Verifique o processo e tente novamente."
  exit 1
fi

# Criar pasta do projeto
mkdir -p $PROJETO_DIR
cd $PROJETO_DIR || { echo "Erro ao acessar o diretório do projeto."; exit 1; }

# Clonar repositório Git e iniciar do zero
if [ -d ".git" ]; then
  git checkout main
  git pull origin main
  git tag -a "backup-$(date +%Y%m%d-%H%M%S)" -m "Backup antes do reinício"
  git push origin --tags
  rm -rf *
fi

git init
git remote add origin $REPO_GIT
touch README.md

# Criar estrutura de pastas do projeto
mkdir -p backend frontend database docker docs tests logs config kubernetes services bi ml monitoring

# Configurar ambiente virtual do Django
cd backend || { echo "Erro ao acessar o diretório backend."; exit 1; }
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
if ! pip install django djangorestframework psycopg2-binary django-cors-headers django-allauth django-environ channels celery django-rest-swagger djangorestframework-simplejwt drf-yasg scikit-learn pandas numpy matplotlib prometheus_client elastic-apm[django]; then
  echo "Erro ao instalar dependências Python."
  exit 1
fi

# Iniciar projeto Django, se não existir
if [ ! -f "manage.py" ]; then
  django-admin startproject ClinicaAI .
fi

# Criar pastas e módulos adicionais
mkdir -p apps
cd apps || { echo "Erro ao acessar o diretório apps."; exit 1; }
for app in pacientes agendamentos financeiro faturamento despesas planilhas documentos assinar_documentos vendas crm assinaturas locacao criador_sites ecommerce blog forum chat_ao_vivo elearning inventario fabricacao plm compras manutencao qualidade recursos_humanos recrutamento folgas avaliacoes indicacoes frota redes_sociais marketing_email marketing_sms eventos automacao_marketing pesquisas projeto planilhas_horas servico_campo central_ajuda compromissos produtividade mensagens aprovacoes iot voip conhecimento whatsapp; do
  if [ ! -d "$app" ]; then
    django-admin startapp $app
  fi
  # Adicionar módulo ao INSTALLED_APPS no settings.py
  if ! grep -q "'apps.${app}'," ../ClinicaAI/settings.py; then
    sed -i "/INSTALLED_APPS = \[/a \ \ \ \ 'apps.${app}'," ../ClinicaAI/settings.py
  fi
done
cd ..

# Adicionar bibliotecas ao settings.py
for lib in rest_framework corsheaders channels drf_yasg prometheus_client elastic_apm.contrib.django; do
  if ! grep -q "'${lib}'," ClinicaAI/settings.py; then
    sed -i "/INSTALLED_APPS = \[/a \ \ \ \ '${lib}'," ClinicaAI/settings.py
  fi
done

# Configurar CORS no settings.py
if ! grep -q "'corsheaders.middleware.CorsMiddleware'" ClinicaAI/settings.py; then
  sed -i "/MIDDLEWARE = \[/a \ \ \ \ 'corsheaders.middleware.CorsMiddleware'," ClinicaAI/settings.py
fi
if ! grep -q "CORS_ALLOWED_ORIGINS" ClinicaAI/settings.py; then
  echo -e "CORS_ALLOWED_ORIGINS = [\n    'http://localhost:3000'\n]" >> ClinicaAI/settings.py
fi

# Configurar banco de dados PostgreSQL no settings.py
sed -i "s/ENGINE': 'django.db.backends.sqlite3'/ENGINE': 'django.db.backends.postgresql'/" ClinicaAI/settings.py
sed -i "s/NAME': BASE_DIR .*/NAME': 'clinicaai',\n        'USER': '$DB_USER',\n        'PASSWORD': '$DB_PASSWORD',\n        'HOST': 'localhost',\n        'PORT': '5432'/" ClinicaAI/settings.py

# Configurar Channels para WebSockets
if ! grep -q "ASGI_APPLICATION" ClinicaAI/settings.py; then
  echo "ASGI_APPLICATION = 'ClinicaAI.asgi.application'" >> ClinicaAI/settings.py
fi
if ! grep -q "CHANNEL_LAYERS" ClinicaAI/settings.py; then
  echo -e "CHANNEL_LAYERS = {\n    'default': {\n        'BACKEND': 'channels_redis.core.RedisChannelLayer',\n        'CONFIG': {\n            'hosts': [('127.0.0.1', 6379)],\n        },\n    },\n}" >> ClinicaAI/settings.py
fi

# Configurar Celery para tarefas em segundo plano
if ! grep -q "CELERY_BROKER_URL" ClinicaAI/settings.py; then
  echo -e "CELERY_BROKER_URL = 'redis://localhost:6379/0'\nCELERY_RESULT_BACKEND = 'redis://localhost:6379/0'" >> ClinicaAI/settings.py
fi

# Configurar JWT para autenticação
if ! grep -q "DEFAULT_AUTHENTICATION_CLASSES" ClinicaAI/settings.py; then
  echo -e "REST_FRAMEWORK = {\n    'DEFAULT_AUTHENTICATION_CLASSES': (\n        'rest_framework_simplejwt.authentication.JWTAuthentication',\n    ),\n    'DEFAULT_PERMISSION_CLASSES': (\n        'rest_framework.permissions.IsAuthenticated',\n    ),\n}" >> ClinicaAI/settings.py
fi

# Criar banco de dados PostgreSQL
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw clinicaai; then
  sudo -u postgres psql -c "CREATE DATABASE clinicaai;"
fi
if ! sudo -u postgres psql -c "\du" | cut -d \| -f 1 | grep -qw $DB_USER; then
  sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
fi
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE clinicaai TO $DB_USER;"

# Realizar migrações iniciais
python manage.py makemigrations
python manage.py migrate

# Criar superusuário Django (opcional: pode ser configurado manualmente depois)
if ! echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists()" | python manage.py shell | grep -q 'True'; then
  echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
fi

# Instalar dependências do frontend
cd $PROJETO_DIR/frontend
if [ ! -d "clinicaai-frontend" ]; then
  npx create-react-app clinicaai-frontend
fi

# Inicializar Docker e Kubernetes
cd $PROJETO_DIR/docker
cat <<EOF > docker-compose.yml
version: '3.1'
services:
  db:
    image: postgres
    restart: always
    environment:
      POSTGRES_USER: $DB_USER
      POSTGRES_PASSWORD: $DB_PASSWORD
      POSTGRES_DB: clinicaai
    ports:
      - "5432:5432"
  redis:
    image: redis
    restart: always
    ports:
      - "6379:6379"
  web:
    build: ../backend
    command: daphne -b 0.0.0.0 -p 8000 ClinicaAI.asgi:application
    volumes:
      - ../backend:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
  worker:
    build: ../backend
    command: celery -A ClinicaAI worker --loglevel=info
    volumes:
      - ../backend:/code
    depends_on:
      - db
      - redis
  frontend:
    image: node
    working_dir: /app
    volumes:
      - ../frontend/clinicaai-frontend:/app
    command: npm start
    ports:
      - "3000:3000"
    depends_on:
      - web
EOF

# Criar configuração Kubernetes para o projeto
cd $PROJETO_DIR/kubernetes
cat <<EOF > clinicaai-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: clinicaai-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: clinicaai
  template:
    metadata:
      labels:
        app: clinicaai
EOF
