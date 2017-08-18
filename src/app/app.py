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
from database import db_session, init_db
from models import User, Role, Repository

DIR_APP = os.path.split(os.path.abspath(__file__))[0]
DIR_TEMPLATES = os.path.join(DIR_APP, 'templates')
FILE_BASE_HTML = os.path.join(DIR_TEMPLATES, 'base.html')
FILE_BASE_HTML_EXAMPLE = os.path.join(DIR_TEMPLATES, 'base.html.example')

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


@app.before_first_request
def app_init():
    init_db()
    

def maybe_create_base_html():
    if not os.path.exists(FILE_BASE_HTML):
        shutil.copy(FILE_BASE_HTML_EXAMPLE, FILE_BASE_HTML)


def main():
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))

    kwargs = dict(host=host, port=port)
    logger.info('Flask config: {}'.format(kwargs))

    maybe_create_base_html()
    app.run(**kwargs)


if __name__ == '__main__':
    main()
