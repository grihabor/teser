import shutil
import logging
import os

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_security import (
    Security, login_required, SQLAlchemySessionUserDatastore,
    current_user
)
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField

from app_config import setup_config
from database import db_session, POSTGRES_URL
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
Bootstrap(app)

# Setup Flask-Mail
mail = Mail(app)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)


def validate_repository(url, branch):
    return True


@app.route('/add_repository')
@login_required
def add_repository():
    url = request.args['url']
    branch = request.args['branch']
    if validate_repository(url, branch):
        repo = Repository(user_id=current_user.id, url=url, branch=branch)
        print(current_user.username)
        try:
            db_session.add(repo)
            db_session.commit()
            result = 'ok'
        except Exception as e:
            logger.warning(e)
            db_session.rollback()
            result = 'invalid repository'
    else:
        result = 'invalid repository'

    return jsonify(dict(
        result=result,
        repositories=[dict(url=repo.url,
                           branch=repo.branch) for repo in current_user.repositories]
    ))


class RepositoryForm(FlaskForm):
    url = StringField(label='URL', validators=[validators.DataRequired()])
    branch = StringField(label='Branch', validators=[validators.DataRequired()])
    submit = SubmitField(label='Add')


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
