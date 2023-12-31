# Overview
PostgresSQL db

# Quickstart
* login with:<br>`docker exec -it ${CONTAINER_NAME} psql -d ${POSTGRES_DB} -U ${POSTGRES_USER} -W`
* once in `psql`, quit with `\q`

# Initializing
* The database and admin user are created if the proper environment variables are passed.
* As an alternative to SQL scripts, we could use a bash script (e.g., `init_alt/init_db.sh`). That might be helpful in other scenarios.
    * I like using SQL scripts to initialize everything because they're easier to copy/paste to/from other tools.