#!/usr/bin/env bash

# constants
TODAY=$(date +"%Y-%m-%d")

# set up
set -e

# Funcs

# execute psql
# $1 = sql string
function execute {
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    $1 
EOSQL
}

# create tables

## texts
execute "
    CREATE TABLE IF NOT EXISTS texts (
        text_id SERIAL PRIMARY KEY,
        dt_entered TIMESTAMP WITH TIME ZONE,
        dt_requested TIMESTAMP WITH TIME ZONE,
        client_host VARCHAR(16),
        text_source VARCHAR(255),
        name VARCHAR(255),
        text_tags VARCHAR(255) ARRAY,
        text TEXT
    );
"

## codes
execute "
    CREATE TABLE IF NOT EXISTS codes (
        code_id SERIAL PRIMARY KEY,
        dt_entered TIMESTAMP WITH TIME ZONE,
        code VARCHAR(255) UNIQUE,
        is_admin BOOLEAN
    );
"

# create users for PostgREST
execute "
    -- 1. set up user for anonymous requests
    create role $SERVER_DB_ANON_ROLE nologin;

    grant usage on schema public to $SERVER_DB_ANON_ROLE;
    grant select on public.texts to $SERVER_DB_ANON_ROLE;
    grant select on public.codes to $SERVER_DB_ANON_ROLE;

    -- 2. dedicated role for connecting to the database

    create role $SERVER_DB_AUTHENTICATOR_USERNAME noinherit login password '$SERVER_DB_AUTHENTICATOR_PASSWORD';
    grant $SERVER_DB_ANON_ROLE to $SERVER_DB_AUTHENTICATOR_USERNAME;

    -- 3. create user with authority to update database

    create role $SERVER_DB_API_USERNAME nologin;
    grant $SERVER_DB_API_USERNAME to $SERVER_DB_AUTHENTICATOR_USERNAME;

    grant usage on schema public to $SERVER_DB_API_USERNAME;
    grant all on public.texts to $SERVER_DB_API_USERNAME;
    grant usage, select on sequence public.texts_text_id_seq to $SERVER_DB_API_USERNAME;
    grant all on public.codes to $SERVER_DB_API_USERNAME;
    grant usage, select on sequence public.codes_code_id_seq to $SERVER_DB_API_USERNAME;
"

# create admin password
execute "
    INSERT INTO public.codes
    (code_id, dt_entered, code, is_admin)
    VALUES(nextval('codes_code_id_seq'::regclass), '$TODAY', '$APP_ADMIN_PASSWORD', True);
"