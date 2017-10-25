import logging

from flask import jsonify
from flask_security import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import join

from database import db_session
from models import Repository, User
from utils import (
    safe_get_repository,
    UIError,
    UnifiedResponse
)
from .activation import import_repository_activate
from .new_repo import import_repository_add
from .list import import_repository_list, user_repositories

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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


def import_repository(app):
    import_repository_add(app)
    import_repository_list(app)
    import_repository_activate(app)

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
