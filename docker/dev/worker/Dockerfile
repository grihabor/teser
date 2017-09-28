FROM grihabor/testing-server:base-flask
MAINTAINER Borodin Gregory <grihabor@mail.ru>

USER nobody

ADD src /project/src

CMD celery -A tasks worker --loglevel=info
