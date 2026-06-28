#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate

echo "Seeding cinema data..."
python manage.py seed_cinema || true

echo "Starting Gunicorn..."

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 4 \
    --threads 2 \
    --log-file -