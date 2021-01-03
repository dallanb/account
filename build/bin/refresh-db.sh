#!/bin/sh

docker exec -it account bash -c "python manage.py reset"
docker exec -it account bash -c "python manage.py init"