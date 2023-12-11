# # Overview
# * build python env for web app
# * execution is handled in docker-compose.yml

FROM python:3.11-slim

# install dependencies
RUN apt-get update
RUN apt-get install -y curl # for health check

# set up working dir
RUN mkdir /usr/src/www
WORKDIR /usr/src/www

# install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy everything
COPY . .