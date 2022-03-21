FROM python:3.9.6-alpine

WORKDIR /computing

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
# RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
COPY ./requirements.txt /computing/
RUN pip install -r requirements.txt

COPY . /computing/