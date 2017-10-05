FROM teser/flask.base:latest
MAINTAINER Borodin Gregory <grihabor@mail.ru>

RUN adduser -s /bin/sh -S -G ping worker
USER worker

ENV PROJECT_ROOT /project
ENV PYTHONPATH $PROJECT_ROOT/src:$PYTHONPATH

VOLUME $PROJECT_ROOT/keys/

WORKDIR $PROJECT_ROOT
ADD src ./src

CMD celery -A tasks worker --loglevel=info
