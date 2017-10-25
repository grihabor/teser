from flask import jsonify
from flask_security import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from database import db_session
from models import User, Repository
from utils import safe_get_repository, UnifiedResponse, UIError
from .repo_list import user_repositories


def maybe_remove_active_repo_ref(repo):
    user = User.query.get(repo.user_id)
    if user.active_repository_id == repo.id:
        user.active_repository_id = None


def remove_repo(repo: Repository):
    try:
        maybe_remove_active_repo_ref(repo)
        db_session.delete(repo)
        db_session.commit()
        result = UnifiedResponse(
            result='ok',
            details=''
        )
    except SQLAlchemyError:
        db_session.rollback()
        result = UnifiedResponse(
            result='fail',
            details='Database error'
        )
    return result


def import_repository_remove(app):
    @app.route('/api/repository/remove')
    @login_required
    def repository_remove():
        try:
            repo = safe_get_repository('id')
            result = remove_repo(repo)
        except UIError as e:
            result = UnifiedResponse(
                result='fail',
                details=str(e)
            )

        result.update(dict(
            repositories=user_repositories(current_user)
        ))
        return jsonify(result)
