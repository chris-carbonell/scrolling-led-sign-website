#!/usr/bin/env bash

# constants
TODAY=$(date +"%Y-%m-%d")

# set up
set -e

# create admin password
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    INSERT INTO public.codes
    (code_id, dt_entered, code, is_admin)
    VALUES(nextval('codes_code_id_seq'::regclass), '$TODAY', '$APP_ADMIN_PASSWORD', True);
EOSQL