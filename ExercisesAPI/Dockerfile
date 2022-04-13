# pull official base image
FROM python:3

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


#install packages for Pillow
# RUN apk add zlib-dev jpeg-dev gcc musl-dev
#install packages for postgres
# RUN apk add python3-dev  
# RUN apk add musl-dev
# install dependencies
# RUN apt install libpq-dev python3-dev
# RUN apt install build-essential
RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000

# copy project
COPY . /usr/src/app/