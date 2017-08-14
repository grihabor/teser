import os

bind = '{}:{}'.format(
    os.getenv('FLASK_HOST'),
    os.getenv('FLASK_PORT')
)
workers = 3
