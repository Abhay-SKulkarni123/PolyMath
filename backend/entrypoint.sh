#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate

echo "Seeding cinema data..."
python manage.py seed_cinema || true

echo "Fixing All In One..."
python manage.py fix_all_in_one || true

echo "Creating vendor & seeding books..."
python manage.py create_vendor_seed_book || true

echo "Seeding featured books..."
python manage.py seed_featured_books || true

echo "Starting Gunicorn..."

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 4 \
    --threads 2 \
    --log-file -