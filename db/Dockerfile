# # Overview
# * build database
# * execution is handled in docker-compose.yml

FROM postgres:16.1

# copy init scripts
COPY ./sql/init/* /docker-entrypoint-initdb.d/