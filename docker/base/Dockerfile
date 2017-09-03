FROM library/python:3.6-alpine3.6
MAINTAINER Borodin Gregory <grihabor@mail.ru>

RUN echo "ipv6" >> /etc/modules

# install service dependencies
RUN apk update \
 && apk --update --no-cache add \
        libpq \
        openssh-client \
        git \
        docker

# install build dependencies, python packages
# then remove build dependencies
RUN apk --update add --virtual build-dependencies \
        libffi-dev \
        python3-dev \
        gcc \
        postgresql-dev \
        musl-dev \
 && pip3 install --no-cache-dir \
        flask==0.12 \
        flask-security==3.0 \
        flask-mail==0.9 \
        flask-bootstrap==3.3.7.1 \
        sqlalchemy==1.1 \
        psycopg2==2.7 \
        alembic==0.9.5 \
        bcrypt==3.1 \
 && apk del build-dependencies

