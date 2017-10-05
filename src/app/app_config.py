import os


def setup_config(app):
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'super-secret'

    # Flask-Mail config
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_SSL'] = bool(int(os.getenv('MAIL_USE_SSL')))
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    # Flask-Security config
    app.config['SECURITY_PASSWORD_SALT'] = 'somesalthere'
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_CONFIRMABLE'] = True
    app.config['SECURITY_EMAIL_SENDER'] = app.config['MAIL_USERNAME']
