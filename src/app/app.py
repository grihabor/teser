import shutil
import logging
import os

from flask import Flask, render_template
from flask_mail import Mail
from flask_security import (
    Security, login_required, SQLAlchemySessionUserDatastore,
    current_user
)

from app_config import setup_config
from database import db_session, init_db, POSTGRES_URL
from models import User, Role, Repository

DIR_APP = os.path.split(os.path.abspath(__file__))[0]
DIR_TEMPLATES = os.path.join(DIR_APP, 'templates')
FILE_BASE_HTML = os.path.join(DIR_TEMPLATES, 'base.html')
FILE_BASE_HTML_EXAMPLE = FILE_BASE_HTML + '.example'

DIR_SRC = os.path.normpath(os.path.join(DIR_APP, os.pardir))
FILE_ALEMBIC_INI = os.path.join(DIR_SRC, 'alembic.ini')
FILE_ALEMBIC_INI_EXAMPLE = FILE_ALEMBIC_INI + '.example'

SQLALCHEMY_URL = 'sqlalchemy.url'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create app
app = Flask(__name__)
setup_config(app)

# Setup Flask-Mail
mail = Mail(app)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)


# Views
@app.route('/home')
@login_required
def home():
    logger.info('Current user: {}'.format(current_user))
    return render_template('home.html',
                           repositories=current_user.repositories)


@app.route('/')
def index():
    return render_template('index.html')


def maybe_create_base_html():
    if not os.path.exists(FILE_BASE_HTML):
        shutil.copy(FILE_BASE_HTML_EXAMPLE, FILE_BASE_HTML)


def maybe_create_alembic_ini():
    if not os.path.exists(FILE_ALEMBIC_INI):
        with open(FILE_ALEMBIC_INI_EXAMPLE, 'r') as example, \
                open(FILE_ALEMBIC_INI, 'w') as ini:
            for line in example:
                if SQLALCHEMY_URL not in line:
                    ini.write(line)
                else:
                    ini.write('{} = {}\n'.format(
                        SQLALCHEMY_URL, POSTGRES_URL
                    ))


def main():
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))

    kwargs = dict(host=host, port=port)
    logger.info('Flask config: {}'.format(kwargs))

    maybe_create_base_html()
    maybe_create_alembic_ini()
    app.run(**kwargs)


if __name__ == '__main__':
    main()
