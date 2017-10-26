from flask import jsonify
from flask_security import login_required, current_user, roles_required
from sqlalchemy import join

from database import db_session
from models import Repository, User


def user_repositories(user: User):
    active_repo_id = user.active_repository_id

    def repo_to_response(repo):
        info = dict(repo)
        info['active'] = (repo.id == active_repo_id)
        return info

    return [repo_to_response(repo)
            for repo in user.repositories]


def active_repositories():
    query = db_session.query(
        Repository
    ).select_from(join(
        User,
        Repository,
        User.active_repository_id == Repository.id
    ))

    return [dict(repo)
            for repo in query.all()]


def import_repository_list(app):
    @app.route('/api/repository/list')
    @login_required
    def repository_list():
        return jsonify(dict(
            repositories=user_repositories(current_user)
        ))

    @app.route('/api/repository/active/list')
    @roles_required('admin')
    def active_repository_list():
        return jsonify(dict(
            active_repositories=active_repositories()
        ))
