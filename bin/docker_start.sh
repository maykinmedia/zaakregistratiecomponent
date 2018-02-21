#!/usr/bin/env bash

# wait for Postgres to start
function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="db")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

source env/bin/activate
python src/manage.py migrate --settings=zaakmagazijn.conf.docker
python src/manage.py collectstatic --noinput --settings=zaakmagazijn.conf.docker
python src/manage.py runserver 0.0.0.0:8000 --settings=zaakmagazijn.conf.docker
