from flask import jsonify
from flask_security import roles_required

from models import User


def import_user(app):
    @app.route('/api/user/list')
    @roles_required('admin')
    def user_list():
        users = User.query.all()
        return jsonify(dict(users=[
            dict(email=user.email,
                 username=user.username,
                 id=user.id,
                 roles=[role.name for role in user.roles])
            for user in users
        ]))
