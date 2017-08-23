FROM library/python:3.5-alpine
MAINTAINER Borodin Gregory <grihabor@mail.ru>

WORKDIR /project

RUN echo "ipv6" >> /etc/modules

RUN apk update                      \
 && apk --no-cache add              \
        libffi-dev                  \
        python3-dev                 \
        gcc                         \
        postgresql-dev              \
        musl-dev                    \
        openssh-client              \
        git                         \
 && pip3 install --no-cache-dir     \
        flask==0.12                 \
        flask-security==3.0         \
        flask-mail==0.9             \
        flask-bootstrap==3.3.7.1    \
        sqlalchemy==1.1             \
        psycopg2==2.7               \
        alembic==0.9.5              \
        bcrypt==3.1

ADD src ./src

EXPOSE 5000
VOLUME /keys

CMD python3 -u /project/src/app/app.py
