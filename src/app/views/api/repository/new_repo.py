import logging

from flask import request, jsonify
from flask_security import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from database import db_session
from models import Repository
from tasks import clone_repository
from utils import UnifiedResponse, process_details
from views.api.repository import user_repositories

logger = logging.getLogger(__name__)


def validate_repository(url, identity_file):
    result = clone_repository.delay(url, identity_file)
    unified_response = result.get()

    logger.info(unified_response)
    return unified_response


def _add_repository(url):
    identity_file = current_user.generated_identity_file

    if identity_file is None:
        return UnifiedResponse(
            result='fail',
            details="Current user doesn't have generated identity file"
        )

    validation = validate_repository(url, identity_file)

    if validation.result == 'ok':
        repo = Repository(user_id=current_user.id,
                          url=url,
                          identity_file=identity_file)
        try:
            db_session.add(repo)
            current_user.active_repository_id = repo.id
            current_user.generated_identity_file = None
            db_session.commit()
            response = UnifiedResponse(
                result='ok',
                details=''
            )
        except SQLAlchemyError:
            db_session.rollback()
            response = UnifiedResponse(
                result='fail',
                details='Failed to save the repository into database'
            )
    else:
        response = UnifiedResponse(
            result='fail',
            details=['Failed to validate the url:'] + process_details(validation.details)
        )

    response.update(dict(
        repositories=user_repositories(current_user)
    ))
    return response


def import_repository_add(app):
    @app.route('/api/repository/add')
    @login_required
    def repository_add():
        url = request.args['url']
        return jsonify(dict(_add_repository(url)))
