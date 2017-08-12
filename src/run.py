import os

if os.getenv('FLASK_DEBUG', 0):
    import importlib
    importlib.import_module('app')
else:
    os.system('gunicorn -c gunicorn_config.py app:app')
