# Overview
PostgresSQL db

# Quickstart
* login with:<br>`docker exec -it ${CONTAINER_NAME} psql -d ${POSTGRES_DB} -U ${POSTGRES_USER} -W`
* once in `psql`, quit with `\q`

# Initializing
* The database and admin user are created if the proper environment variables are passed.