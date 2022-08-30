FROM python:3.10

WORKDIR /app/src

RUN apt-get update && pip install --upgrade pip && pip install poetry

COPY . /app/src

RUN poetry config virtualenvs.create false && poetry install
