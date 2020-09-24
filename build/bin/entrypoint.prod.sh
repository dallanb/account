#!/bin/sh

. ~/.bashrc

pip install -e .

if [ "$DATABASE" = "account" ]; then
  echo "Waiting for account..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

if [ ! -d "migrations/prod/versions" ]; then
  echo "Directory migrations/prod/versions does not exist."
  flask db init --directory=migrations/prod
  sed -i '/import sqlalchemy as sa/a import sqlalchemy_utils' migrations/prod/script.py.mako
  flask db migrate --directory=migrations/prod
fi

flask db upgrade --directory=migrations/prod


gunicorn --bind 0.0.0.0:5000 manage:app