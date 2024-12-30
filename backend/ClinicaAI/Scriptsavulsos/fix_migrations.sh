#!/bin/bash

# Ativando o ambiente virtual
source .venv/Scripts/activate

# Conectando ao banco de dados para limpar o histórico de migrações
echo "Limpando histórico de migrações no banco de dados..."
psql -U postgres -d clinicaai -h localhost -p 5432 <<EOF
DELETE FROM django_migrations WHERE app='prontuarios';
DELETE FROM django_migrations WHERE app='assinaturas';
DELETE FROM django_migrations WHERE app='pacientes';
DROP TABLE IF EXISTS prontuarios_prontuario;
DROP TABLE IF EXISTS assinaturas_assinatura;
DROP TABLE IF EXISTS pacientes_paciente;
EOF

# Recriando as migrações
echo "Recriando as migrações..."
python manage.py makemigrations assinaturas
python manage.py makemigrations prontuarios
python manage.py makemigrations pacientes

# Aplicando as migrações
echo "Aplicando as migrações..."
python manage.py migrate

# Iniciando o servidor para verificar se está tudo funcionando
echo "Iniciando o servidor..."
python manage.py runserver
