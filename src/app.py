import logging
import os
from flask import Flask
from flask_security import (
    Security, login_required, SQLAlchemySessionUserDatastore
)
from database import db_session, init_db
from models import User, Role


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'somesalthere'
app.config['SECURITY_REGISTERABLE'] = True

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)


# Create a user to test with
@app.before_first_request
def create_user():
    init_db()

    kwargs = dict(
        email='example@gmail.com',
        password='password',
    )

    if not user_datastore.find_user(**kwargs):
        user_datastore.create_user(**kwargs)
        db_session.commit()

# Views
@app.route('/')
@login_required
def home():
    return 'Here you go!'

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))

    kwargs = dict(host=host, port=port)
    logger.info('Flask config: {}'.format(kwargs))
    app.run(**kwargs)

    app.run(host=host, port=port)
