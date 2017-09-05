import json
import logging
import urllib

from flask import request, jsonify
from flask_security import login_required, current_user

from database import db_session
from models import Repository
from util import safe_get_repository, RepositoryError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UnifiedResponse:
    def __init__(self, *, result, details):
        self.result = result
        self.details = details

    def __iter__(self):
        yield 'result', self.result
        yield 'details', self.details


def validate_repository(url, identity_file):
    path = 'http://{host}:{port}/clone_repo?url={url}&identity_file={identity_file}'.format(
        host='tester',
        port=6000,
        url=url,
        identity_file=identity_file
    )

    with urllib.request.urlopen(path) as f:
        data = json.loads(f.read().decode('utf-8'))

    logger.info(data)
    return data


def process_details(details):
    if type(details) not in [str, list]:
        raise ValueError('details must be {} or {}'.format(str, list))

    if type(details) is list:
        return [process_details(part)
                for part in details]
    elif type(details) is str:
        return details.split('\n')


def _add_repository(url):
    identity_file = current_user.generated_identity_file

    if identity_file is None:
        return UnifiedResponse(
            result='fail',
            details="Current user doesn't have generated identity file"
        )

    validation = validate_repository(url, identity_file)

    if validation['ok']:
        repo = Repository(user_id=current_user.id,
                          url=url,
                          identity_file=identity_file)
        try:
            db_session.add(repo)
            current_user.generated_identity_file = None
            db_session.commit()
            response = UnifiedResponse(result='ok',
                                       details='')
        except Exception as e:
            logger.warning(e)
            db_session.rollback()
            response = UnifiedResponse(
                result='fail',
                details='Failed to save the repository into database'
            )
    else:
        response = UnifiedResponse(
            result='fail',
            details=['Failed to validate the url:'] + process_details(validation['details'])
        )

    return jsonify(dict(response).update(
        repositories=[dict(id=repo.id,
                           url=repo.url,
                           identity_file=repo.identity_file)
                      for repo in current_user.repositories]
    ))


def remove_repo(repo):
    try:
        db_session.delete(repo)
        db_session.commit()
    except Exception as e:
        logger.warning(e)
        return UnifiedResponse(
            result='fail',
            details='Database error'
        )

    return UnifiedResponse(result='ok',
                           details='')


def user_repositories(user):
    return [dict(url=repo.url,
                 identity_file=repo.identity_file,
                 id=repo.id)
            for repo in user.repositories]


def import_repository(app):
    @app.route('/api/repository/add')
    @login_required
    def repository_add():
        url = request.args['url']
        return _add_repository(url)

    @app.route('/api/repository/list')
    @login_required
    def repository_list():
        return jsonify(dict(
            repositories=user_repositories(current_user)
        ))

    @app.route('/api/repository/remove')
    @login_required
    def repository_remove():
        try:
            repo = safe_get_repository('id')
            result = remove_repo(repo)
        except RepositoryError as e:
            result = UnifiedResponse(
                result='fail',
                details=str(e)
            )

        return jsonify(dict(result).update(
            user_repositories(current_user))
        )
