#!/bin/bash

# Variáveis de configuração
DB_USER="diego"
DB_PASSWORD="Mouse2250@#86"
PROJETO_DIR="/mnt/dados/ClinicaAI"

# Verificar se Docker está instalado e iniciar Docker Compose
if ! command -v docker &> /dev/null; then
  echo "Docker não está instalado corretamente. Verifique a instalação do Docker antes de continuar."
  exit 1
fi
if ! command -v docker-compose &> /dev/null; then
  echo "Docker Compose não está instalado corretamente. Verifique a instalação do Docker Compose antes de continuar."
  exit 1
fi

# Voltar ao diretório do projeto
cd $PROJETO_DIR/docker || { echo "Erro ao acessar o diretório docker."; exit 1; }

# Criar docker-compose.yml
cat <<EOF > docker-compose.yml
version: '3.1'
services:
  db:
    image: postgres:13
    restart: always
    environment:
      POSTGRES_USER: $DB_USER
      POSTGRES_PASSWORD: $DB_PASSWORD
      POSTGRES_DB: clinicaai
    ports:
      - "5432:5432"
  redis:
    image: redis:6
    restart: always
    ports:
      - "6379:6379"
  web:
    image: python:3.9
    working_dir: /code
    volumes:
      - ../backend:/code
    command: bash -c "pip install -r requirements.txt && daphne -b 0.0.0.0 -p 8000 ClinicaAI.asgi:application"
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
  worker:
    image: python:3.9
    working_dir: /code
    volumes:
      - ../backend:/code
    command: bash -c "pip install -r requirements.txt && celery -A ClinicaAI worker --loglevel=info"
    depends_on:
      - db
      - redis
  frontend:
    image: node:14
    working_dir: /app
    volumes:
      - ../frontend/clinicaai-frontend:/app
    command: npm start
    ports:
      - "3000:3000"
    depends_on:
      - web
EOF

# Inicializar Docker com timeout de 5 minutos
if ! timeout 300 docker-compose up -d; then
  echo "Erro ao inicializar os serviços Docker ou tempo limite excedido. Verifique o Docker Compose."
  exit 1
fi

# Verificar se os serviços estão sendo construídos corretamente
docker-compose logs -f &

# Aguardar os serviços estarem prontos
sleep 30

# Configurar Kubernetes para o projeto
cd $PROJETO_DIR/kubernetes || { echo "Erro ao acessar o diretório Kubernetes."; exit 1; }
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
    spec:
      containers:
      - name: clinicaai-web
        image: python:3.9
        ports:
        - containerPort: 8000
      - name: redis
        image: redis:6
        ports:
        - containerPort: 6379
      - name: postgres
        image: postgres:13
        env:
        - name: POSTGRES_USER
          value: "$DB_USER"
        - name: POSTGRES_PASSWORD
          value: "$DB_PASSWORD"
        - name: POSTGRES_DB
          value: "clinicaai"
EOF

# Aplicar configuração Kubernetes (necessita kubectl e acesso configurado ao cluster)
if ! kubectl apply -f clinicaai-deployment.yaml; then
  echo "Erro ao aplicar as configurações no Kubernetes. Verifique se o kubectl está configurado corretamente."
  exit 1
fi

# Configuração do Prometheus e Grafana
cd $PROJETO_DIR/monitoring || { echo "Erro ao acessar o diretório monitoring."; exit 1; }
cat <<EOF > prometheus.yml
scrape_configs:
  - job_name: 'django'
    static_configs:
      - targets: ['localhost:8000']
EOF

cat <<EOF > grafana-datasource.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://localhost:9090
EOF

# Executar Prometheus e Grafana via Docker
if ! docker run -d -p 9090:9090 -v $PROJETO_DIR/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus; then
  echo "Erro ao iniciar o Prometheus."
  exit 1
fi
if ! docker run -d -p 3000:3000 grafana/grafana; then
  echo "Erro ao iniciar o Grafana."
  exit 1
fi

# Mensagem de conclusão
echo "Configuração concluída. Todos os serviços devem estar em execução. Verifique o painel do Kubernetes e o Docker para confirmar."
