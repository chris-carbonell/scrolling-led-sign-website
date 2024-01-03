# # Overview
# * build python env for app

FROM python:3.11-slim

# ports
EXPOSE 8501

# install dependencies
RUN apt-get update
RUN pip install --upgrade pip

# set up working dir
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# setup streamlit
RUN mkdir -p /root/.streamlit
COPY config.toml /root/.streamlit/config.toml

# copy app
COPY constants.py .
COPY giphy.py .
COPY app.py .

CMD ["streamlit", "run", "app.py", "--server.baseUrlPath=/sign"]