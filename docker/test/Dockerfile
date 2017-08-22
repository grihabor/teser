FROM library/python:3.5-alpine3.4
MAINTAINER Borodin Gregory <grihabor@mail.ru>

WORKDIR /project

RUN echo "ipv6" >> /etc/modules

RUN apk update \
 && apk add \
        libffi-dev \
        python3-dev \
        gcc \
        postgresql-dev \
        musl-dev

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install gunicorn

ADD src ./src

EXPOSE 5000
WORKDIR /project/src/app

CMD gunicorn --config gunicorn_config.py app:app
