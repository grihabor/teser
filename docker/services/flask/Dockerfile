FROM tesver/flask.base:latest
MAINTAINER Borodin Gregory <grihabor@mail.ru>

ENV PROJECT_ROOT /project
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT/src
ENV APP_PORT 5000
ENV KEYS_PATH $PROJECT_ROOT/keys

EXPOSE $APP_PORT
VOLUME $KEYS_PATH

WORKDIR $PROJECT_ROOT

ADD src ./src

CMD python3 -u ./src/app/run_startup.py && python3 -u ./src/app/app.py
