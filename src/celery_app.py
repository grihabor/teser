import os
from celery import Celery

user = os.environ['RABBITMQ_DEFAULT_USER']
password = os.environ['RABBITMQ_DEFAULT_PASS']
vhost = os.environ['RABBITMQ_DEFAULT_VHOST']
host = 'rabbitmq:5672'

app = Celery('tasks', broker=f'amqp://{user}:{password}@{host}/{vhost}')


