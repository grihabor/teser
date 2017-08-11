FROM library/python:3.5
MAINTAINER Borodin Gregory <grihabor@mail.ru>

WORKDIR /project

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ADD src ./src

EXPOSE 5000

CMD python3 -u /project/src/app.py
