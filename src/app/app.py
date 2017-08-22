import subprocess
import logging
import os
import uuid

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_security import (
    Security, login_required, SQLAlchemySessionUserDatastore,
    current_user
)
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField

from app_config import setup_config
from database import db_session
import init
from models import User, Role, Repository


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


DIR_KEYS = '/keys'

def validate_repository(url):
    return True


@app.route('/add_repository')
@login_required
def add_repository():
    url = request.args['url']
    identity_file = current_user.generated_identity_file

    if identity_file is None:
        return "", 500

    if validate_repository(url):
        repo = Repository(user_id=current_user.id,
                          url=url,
                          identity_file=identity_file)
        try:
            db_session.add(repo)
            current_user.generated_identity_file = None
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
        repositories=[dict(url=repo.url)
                      for repo in current_user.repositories]
    ))


@app.route('/generate_deploy_key', methods=['GET'])
@login_required
def generate_deploy_key():
    identity_file = current_user.generated_identity_file

    if identity_file is None:
        identity_file = str(uuid.uuid4())
        path = os.path.join(DIR_KEYS, '{}'.format(identity_file))
        subprocess.run(['ssh-keygen',
                        '-q',
                        '-t', 'rsa',
                        '-b', '2048',
                        '-N', identity_file,
                        '-f', path])
        logger.info('Generated: {}'.format(identity_file))

        try:
            current_user.generated_identity_file = identity_file
            db_session.commit()
        except Exception as e:
            logger.warning(e)
            db_session.rollback()
            return "", 500
    else:
        path = os.path.join(DIR_KEYS, '{}'.format(identity_file))
        logger.info('Use saved one: {}'.format(identity_file))

    with open(path + '.pub', 'r') as f:
        public_key = f.read()
    return jsonify(dict(deploy_key=public_key))


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

    init.init()
    app.run(**kwargs)


if __name__ == '__main__':
    main()
