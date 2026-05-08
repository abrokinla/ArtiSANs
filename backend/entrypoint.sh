#!/bin/sh
set -e

# Wait for DB (optional) - simple loop can be expanded for Postgres
echo "Starting entrypoint..."

# Apply database migrations
echo "Applying database migrations (if any)"
python manage.py migrate --noinput || true

# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

exec "$@"
