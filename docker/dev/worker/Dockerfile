FROM grihabor/testing-server:base-flask
MAINTAINER Borodin Gregory <grihabor@mail.ru>

USER nobody
ENV PROJECT_ROOT /project
ENV PYTHONPATH $PROJECT_ROOT/src:$PYTHONPATH

WORKDIR $PROJECT_ROOT
ADD src ./src

CMD celery -A tasks worker --loglevel=info
