from flask import render_template
from flask_security import roles_required


def import_admin_page(app):
    @app.route('/admin_page')
    @roles_required('admin')
    def admin_page():
        return render_template(
            'admin_page.html',
            script_list=[
                'js/utils/tab_view.jsx',
                'js/utils/table_view.jsx',
                'js/admin_page/testing_panel.jsx',
                'js/admin_page/active_repository_list.jsx',
                'js/admin_page/user_list.jsx',
                'js/admin_page/index.jsx',
            ]
        )
