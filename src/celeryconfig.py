import os
from database import POSTGRES_URL


def broker_connection_string():
    user = os.getenv('RABBITMQ_DEFAULT_USER')
    password = os.getenv('RABBITMQ_DEFAULT_PASS')
    vhost = os.getenv('RABBITMQ_DEFAULT_VHOST')
    host = 'rabbitmq'
    port = '5672'
    return f'amqp://{user}:{password}@{host}:{port}/{vhost}'


broker_url = broker_connection_string()
result_backend = f'db+{POSTGRES_URL}'

