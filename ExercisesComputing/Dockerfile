# pull official base image
FROM openjdk:17-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
# install python
RUN apk add python3 && apk add py3-pip	
# install node
RUN apk add --update nodejs npm
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install -r requirements.txt

EXPOSE 8002
# copy project
COPY . /usr/src/app/




