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


gunicorn --bind 0.0.0.0:5000 manage:app