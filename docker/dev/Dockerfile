FROM grihabor/testing-server:base-flask
MAINTAINER Borodin Gregory <grihabor@mail.ru>

WORKDIR /project

EXPOSE 5000
VOLUME /project/keys

ADD src ./src

CMD python3 -u /project/src/app/app.py
