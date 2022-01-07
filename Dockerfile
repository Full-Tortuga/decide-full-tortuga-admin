# syntax=docker/dockerfile:1
FROM node:14 as build
COPY ./decide/administration/frontend /src
WORKDIR /src
RUN npm i -y
RUN npm run build

FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

RUN apt-get update
RUN apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./decide .
COPY --from=build /src/build ./administration/build
