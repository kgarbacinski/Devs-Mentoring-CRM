# pull official base image
FROM python:3.9.5-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


#install packages for Pillow
RUN apk add zlib-dev jpeg-dev gcc musl-dev
# install dependencies
RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000

# copy project
COPY . /usr/src/app/

