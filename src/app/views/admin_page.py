from flask import render_template
from flask_security import roles_required


def import_admin_page(app):
    @app.route('/admin_page')
    @roles_required('admin')
    def admin_page():
        return render_template('admin_page.html')
