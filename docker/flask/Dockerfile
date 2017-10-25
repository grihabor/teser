FROM tesver/flask.base:latest
MAINTAINER Borodin Gregory <grihabor@mail.ru>

ENV PROJECT_ROOT /project
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT/src
ENV APP_PORT 5000

EXPOSE $APP_PORT
VOLUME $PROJECT_ROOT/keys

WORKDIR $PROJECT_ROOT

ADD src ./src

CMD python3 -u ./src/app/run_startup.py && python3 -u ./src/app/app.py
