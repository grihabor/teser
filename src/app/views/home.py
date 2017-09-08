import logging

from flask import render_template, url_for
from flask_security import login_required, current_user, roles_required
from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, SubmitField

logger = logging.getLogger(__name__)


class RepositoryForm(FlaskForm):
    url = StringField(label='URL',
                      validators=[validators.DataRequired()],
                      description='Example: user@gitlab.com:/user/project')
    deploy_key = TextAreaField(label='Public key',
                               description='Add this key to your project "Deploy keys"')
    submit_button = SubmitField(label='Add')


def import_home(app):
    # Views
    @app.route('/home', methods=['GET', 'POST'])
    @login_required
    def home():
        logger.info('Current user: {0}, roles: {0.roles}'.format(current_user))
        admin_page = url_for('admin_page') if current_user.has_role('admin') else ''
        form = RepositoryForm()
        return render_template('home.html',
                               form=form,
                               repositories=current_user.repositories,
                               admin_page=admin_page)

