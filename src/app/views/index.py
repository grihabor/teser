from flask import render_template


def import_index(app):
    @app.route('/')
    def index():
        return render_template('index.html')
