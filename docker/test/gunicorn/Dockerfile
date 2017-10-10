FROM tesver/flask.base:latest
MAINTAINER Borodin Gregory <grihabor@mail.ru>

RUN pip3 install --no-cache-dir gunicorn

ENV PROJECT_ROOT /project
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT/src
ENV WEB_PORT 5000
ENV KEYS_PATH /keys

EXPOSE $WEB_PORT
VOLUME $KEYS_PATH

WORKDIR $PROJECT_ROOT
ADD docker/dev/gunicorn/gunicorn_config.py .
ADD src ./src

WORKDIR $PROJECT_ROOT/src/app

CMD ["/bin/sh", "-c", "gunicorn --config ${PROJECT_ROOT}/gunicorn_config.py app:app"]
