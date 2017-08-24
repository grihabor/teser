import logging
import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_security import (
    Security, login_required, SQLAlchemySessionUserDatastore,
    current_user
)
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField

import init
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


class RepositoryForm(FlaskForm):
    url = StringField(label='URL',
                      validators=[validators.DataRequired()])
    deploy_key = TextAreaField(label='Public key',
                               description='Add this key to your project "Deploy keys"')
    submit_button = SubmitField(label='Add')


# Views
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    logger.info('Current user: {}'.format(current_user))
    form = RepositoryForm()
    return render_template('home.html',
                           form=form,
                           repositories=current_user.repositories)


@app.route('/')
def index():
    return render_template('index.html')


def main():
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))

    kwargs = dict(host=host, port=port)
    logger.info('Flask config: {}'.format(kwargs))

    app.run(**kwargs)


init.init()
if __name__ == '__main__':
    main()
