import os

def broker_connection_string():
    user = os.environ['RABBITMQ_DEFAULT_USER']
    password = os.environ['RABBITMQ_DEFAULT_PASS']
    vhost = os.environ['RABBITMQ_DEFAULT_VHOST']
    host = 'rabbitmq'
    port = '5672'
    return f'amqp://{user}:{password}@{host}:{port}/{vhost}'

broker_url = broker_connection_string()


