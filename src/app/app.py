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
from app_config import setup_config
from database import db_session
from models import User, Role

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
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

views.import_views(app)


@app.before_first_request
def run():
    admins = os.getenv('ADMINS', None)
    if not admins:
        return

    logger.info('Creating admins: {}'.format(admins))

    try:
        admin_role = user_datastore.find_or_create_role('admin')
        for admin_email in admins.split(','):
            admin = user_datastore.get_user(admin_email)
            if admin:
                user_datastore.add_role_to_user(admin, admin_role)
        user_datastore.commit()
    except Exception as e:
        logger.warning('Failed to initialize admins: {}'.format(e))


def main():
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))

    kwargs = dict(host=host, port=port)
    logger.info('Flask config: {}'.format(kwargs))

    logger.info('Starting flask...')
    app.run(**kwargs)


startup.init()
if __name__ == '__main__':
    main()
