# # Overview
# * build python env for api

FROM python:3.11-slim

# install dependencies
RUN apt-get update
RUN apt-get install -y curl # for health check
RUN apt-get install -y libpq-dev gcc
RUN pip install --upgrade pip

# set up working dir
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy everything
COPY . .

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--log-config=log_conf.yaml", "--timeout-keep-alive=0", "--reload"]