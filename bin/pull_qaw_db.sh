#!/bin/bash

ssh -i /home/dallanbhatti/.ssh/github super_dallan@mega <<EOF
  docker exec account_db pg_dump -c -U "$1" account > account.sql
EOF
rsync -chavzP --stats --remove-source-files super_dallan@mega:/home/super_dallan/account.sql "$HUNCHO_DIR"/services/account/account.sql

docker exec -i account_db psql -U "$1" account <"$HUNCHO_DIR"/services/account/account.sql
