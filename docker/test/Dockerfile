FROM grihabor/testing-server:base-flask
MAINTAINER Borodin Gregory <grihabor@mail.ru>

RUN pip3 install gunicorn

WORKDIR /project
ADD src ./src

EXPOSE 5000
VOLUME /keys

WORKDIR /project/src/app

CMD gunicorn --config gunicorn_config.py app:app
