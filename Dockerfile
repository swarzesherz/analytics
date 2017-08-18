FROM python:3.5.2

MAINTAINER tecnologia@scielo.org

RUN apt-get update && apt-get install -y libmemcached-dev

COPY . /app
COPY production.ini-TEMPLATE /app/config.ini

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install gunicorn

ENV ANALYTICS_SETTINGS_FILE=/app/config.ini

RUN python setup.py install
