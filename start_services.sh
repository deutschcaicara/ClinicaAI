#!/bin/bash

# Verifica se o Redis está rodando
if ! pgrep redis-server > /dev/null; then
    echo "Iniciando Redis..."
    redis-server --daemonize yes
else
    echo "Redis já está em execução."
fi

# Ativa o ambiente virtual
echo "Ativando ambiente virtual..."
source /home/diego/ClinicaAI/venv/bin/activate

# Verifica se o Celery Worker está rodando
if ! pgrep -f "celery worker" > /dev/null; then
    echo "Iniciando Celery Worker..."
    celery -A ClinicaAI worker --loglevel=info &
else
    echo "Celery Worker já está em execução."
fi

# Verifica se o Celery Beat está rodando
if ! pgrep -f "celery beat" > /dev/null; then
    echo "Iniciando Celery Beat..."
    celery -A ClinicaAI beat --loglevel=info &
else
    echo "Celery Beat já está em execução."
fi

# Verifica se o Django está rodando
if ! pgrep -f "manage.py runserver" > /dev/null; then
    echo "Iniciando Servidor Django..."
    python /home/diego/ClinicaAI/backend/manage.py runserver 0.0.0.0:8000 &
else
    echo "Servidor Django já está em execução."
fi
