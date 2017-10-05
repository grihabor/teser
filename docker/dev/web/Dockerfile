FROM teser/flask.base:latest
MAINTAINER Borodin Gregory <grihabor@mail.ru>

ENV PROJECT_ROOT /project
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT/src
ENV TESER_PORT 5000

EXPOSE $TESER_PORT
VOLUME $PROJECT_ROOT/keys

WORKDIR $PROJECT_ROOT

ADD src ./src

CMD python3 -u $PROJECT_ROOT/src/app/app.py
