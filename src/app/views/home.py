import logging

from flask import render_template
from flask_security import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, SubmitField

logger = logging.getLogger(__name__)


class RepositoryForm(FlaskForm):
    url = StringField(label='URL',
                      validators=[validators.DataRequired()])
    deploy_key = TextAreaField(label='Public key',
                               description='Add this key to your project "Deploy keys"')
    submit_button = SubmitField(label='Add')


def import_home(app):
    # Views
    @app.route('/home', methods=['GET', 'POST'])
    @login_required
    def home():
        logger.info('Current user: {}'.format(current_user))
        form = RepositoryForm()
        return render_template('home.html',
                               form=form,
                               repositories=current_user.repositories)
