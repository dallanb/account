#!/bin/sh

. ~/.bashrc

if [ "$DATABASE" = "auth" ]; then
  echo "Waiting for auth..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi


if [ ! -d "migrations/account/versions" ]; then
  echo "Directory migrations/account/versions does not exist."
  flask db init --directory=migrations/account
  sed -i '/import sqlalchemy as sa/a import sqlalchemy_utils' migrations/account/script.py.mako
fi

flask db migrate --directory=migrations/account
flask db upgrade --directory=migrations/account

pip install -e .

gunicorn --bind 0.0.0.0:5000 manage:app
