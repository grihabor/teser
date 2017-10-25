FROM tesver/flask.base:latest
MAINTAINER Borodin Gregory <grihabor@mail.ru>

RUN pip3 install --no-cache-dir gunicorn

ENV PROJECT_ROOT /project
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT/src
ENV APP_PORT 5000
ENV KEYS_PATH $PROJECT_ROOT/keys

EXPOSE $APP_PORT
VOLUME $KEYS_PATH

WORKDIR $PROJECT_ROOT
ADD docker/services/gunicorn/gunicorn_config.py .
ADD src ./src

WORKDIR $PROJECT_ROOT/src/app

CMD ["/bin/sh", "-c", "python3 -u ./run_startup.py && gunicorn --config ${PROJECT_ROOT}/gunicorn_config.py app:app"]
