#!/bin/bash

# until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
#     >&2 echo "Postgres is unavailable - sleeping"
#     sleep 1
# done

# >&2 echo "Postgres is up - executing command"

# poetry run task makemigrations
# poetry run task migrate
# poetry run task collectstatic
# poetry run task addjson
# poetry run task createsuperuser --noinput
gunicorn expert_system.wsgi:application --bind 0:8000

exec "$@"