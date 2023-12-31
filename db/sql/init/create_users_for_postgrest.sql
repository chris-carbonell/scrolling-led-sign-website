-- # Overview
-- create and set up users for use with PostgREST

-- # Resources
-- https://postgrest.org/en/stable/tutorials/tut0.html
-- https://postgrest.org/en/stable/tutorials/tut1.html

-- 1. set up user for anonymous requests
 
create role web_anon nologin;

grant usage on schema public to web_anon;
grant select on public.texts to web_anon;
grant select on public.codes to web_anon;

-- 2. dedicated role for connecting to the database

create role authenticator noinherit login password 'fI13C0q9b+=i';
grant web_anon to authenticator;

-- 3. create user with authority to update database

create role api_user nologin;
grant api_user to authenticator;

grant usage on schema public to api_user;
grant all on public.texts to api_user;
grant usage, select on sequence public.texts_text_id_seq to api_user;
grant all on public.codes to api_user;
grant usage, select on sequence public.codes_code_id_seq to api_user;