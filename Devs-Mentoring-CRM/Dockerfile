FROM python:3.9.6-alpine

WORKDIR /crm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
COPY ./requirements.txt /crm/
RUN pip install -r requirements.txt

COPY . /crm/