# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update
RUN apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev

RUN git clone https://github.com/Full-Tortuga/decide-full-tortuga-admin.git .
RUN pip3 install -r requirements.txt

WORKDIR /app/decide

# local settings.py
ADD docker-settings.py /app/decide/local_settings.py
ADD .env /app/decide/.env
