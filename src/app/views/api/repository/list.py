from flask_security import login_required, current_user
from flask import jsonify


def user_repositories(user):
    return [dict(repo)
            for repo in user.repositories]


def import_repository_list(app):
    @app.route('/api/repository/list')
    @login_required
    def repository_list():
        return jsonify(dict(
            repositories=user_repositories(current_user)
        ))
