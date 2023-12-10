FROM python:3.11-slim

# install dependencies
RUN apt-get update
RUN apt-get install -y libpq-dev gcc

# set up working dir
RUN mkdir /usr/src/api
WORKDIR /usr/src/api

# install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy everything
COPY . .