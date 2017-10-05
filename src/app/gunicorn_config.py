import os

host = os.getenv('FLASK_HOST')
port = os.getenv('FLASK_PORT')
bind = f'{host}:{port}'
workers = 2
