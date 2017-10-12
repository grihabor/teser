import logging
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_security import (
    Security, SQLAlchemySessionUserDatastore
)

import startup
import views
import tasks
from app_config import setup_config
from database import db_session
from models import User, Role
from datastore import user_datastore


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create app
app = Flask(__name__)
setup_config(app)
Bootstrap(app)

# Setup Flask-Mail
mail = Mail(app)

# Setup Flask-Security
security = Security(app, user_datastore)

views.import_views(app)


def main():
    host = '0.0.0.0'
    port = int(os.environ['APP_PORT'])

    kwargs = dict(host=host, port=port)
    logger.info('Flask config: {}'.format(kwargs))

    logger.info('Starting flask...')
    app.run(**kwargs)


if __name__ == '__main__':
    main()
