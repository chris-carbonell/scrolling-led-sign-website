# # Overview
# * build python env for api
# * execution is handled in docker-compose.yml

FROM python:3.11-slim

# install dependencies
RUN apt-get update
RUN apt-get install -y curl # for health check
RUN apt-get install -y libpq-dev gcc

# set up working dir
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy everything
COPY . .