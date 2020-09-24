#!/bin/sh

docker exec -it account bash -c "python manage.py reset_db"
docker exec -it account bash -c "python manage.py init"