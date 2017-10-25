from flask import jsonify
from flask_security import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from database import db_session
from utils import safe_get_repository, UnifiedResponse
from .repo_list import user_repositories


def import_repository_activate(app):
    @app.route('/api/repository/activate')
    @login_required
    def activate_repository():
        repo = safe_get_repository('id')  # type: Repository
        try:
            user = repo.user
            user.active_repository_id = repo.id
            db_session.commit()
            result = UnifiedResponse(result='ok',
                                     details='Changed user active repository')

        except SQLAlchemyError:
            db_session.rollback()
            result = UnifiedResponse(result='fail',
                                     details='Database error')

        result.update(dict(
            repositories=user_repositories(current_user)
        ))
        return jsonify(result)
