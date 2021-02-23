#!/bin/sh

. ~/.bashrc

pip install -e .

if [ ! -d "migrations/versions" ]; then
  echo "Directory migrations/versions does not exist."
  flask db init --directory=migrations
  sed -i '/import sqlalchemy as sa/a import sqlalchemy_utils' migrations/script.py.mako
fi

flask db migrate --directory=migrations
flask db upgrade --directory=migrations

gunicorn --bind 0.0.0.0:5000 manage:app
