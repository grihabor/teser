import os

host = '0.0.0.0'
port = os.environ['APP_PORT']
bind = f'{host}:{port}'
workers = 2
