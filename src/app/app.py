import shutil
import logging
import os

from flask import Flask, render_template
from flask_mail import Mail
from flask_security import (
    Security, login_required, SQLAlchemySessionUserDatastore,
    current_user
)
from database import db_session, init_db
from models import User, Role


DIR_APP = os.path.split(os.path.abspath(__file__))[0]
DIR_TEMPLATES = os.path.join(DIR_APP, 'templates')
FILE_BASE_HTML = os.path.join(DIR_TEMPLATES, 'base.html')
FILE_BASE_HTML_EXAMPLE = os.path.join(DIR_TEMPLATES, 'base.html.example')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'

# Setup Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_SSL'] = bool(os.getenv('MAIL_USE_SSL'))
# app.config['MAIL_USE_TLS'] = bool(os.getenv('MAIL_USE_TLS'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

# Setup Flask-Security
app.config['SECURITY_PASSWORD_SALT'] = 'somesalthere'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_EMAIL_SENDER'] = app.config['MAIL_USERNAME']
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)


# Views
@app.route('/home')
@login_required
def home():
    logger.info('Current user: {}'.format(current_user))
    return render_template('home.html')


@app.route('/')
def index():
    return render_template('index.html')


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
