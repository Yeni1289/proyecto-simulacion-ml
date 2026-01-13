#!/bin/bash
set -e

echo "🔄 Ejecutando migraciones..."
python manage.py migrate

echo "📓 Convirtiendo notebooks..."
python convert_notebooks.py

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Iniciando gunicorn..."
exec gunicorn app.wsgi
