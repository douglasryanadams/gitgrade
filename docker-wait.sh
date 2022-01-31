#!/bin/sh
# wait-for-postgres.sh, from: https://docs.docker.com/compose/startup-order/

set -e

until PGPASSWORD="${DATABASE_PASSWORD}" psql -h "${DATABASE_HOST}" -U "${DATABASE_USERNAME}" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - running migrations and executing command"

python -m django migrate
exec "$@"