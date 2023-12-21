# # Overview
# * build python env for app

FROM python:3.11-slim

# ports
EXPOSE 8501

# setup streamlit
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

# install dependencies
RUN apt-get update
RUN pip install --upgrade pip

# set up working dir
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy everything
COPY . .

CMD ["streamlit", "run", "app.py"]