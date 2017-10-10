import os

host = os.getenv('APP_HOST')
port = os.getenv('APP_PORT')
bind = f'{host}:{port}'
workers = 2
