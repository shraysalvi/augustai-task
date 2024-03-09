FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y --no-install-recommends

RUN pip install --upgrade pip pipenv

COPY . .

RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt