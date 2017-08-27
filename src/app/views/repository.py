import json
import logging
import urllib

from flask import request, jsonify
from flask_security import login_required, current_user

from database import db_session
from models import Repository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def validate_repository(url, identity_file):
    path = 'http://{host}:{port}/clone_repo?url={url}&identity_file={identity_file}'.format(
        host='tester',
        port=6000,
        url=url,
        identity_file=identity_file
    )

    with urllib.request.urlopen(path) as r:
        data = json.load(r)

    logger.info(data)
    return data


def _add_repository(url):
    identity_file = current_user.generated_identity_file

    if identity_file is None:
        return "", 500

    validation = validate_repository(url, identity_file)
    details = ''
    if validation['ok']:
        repo = Repository(user_id=current_user.id,
                          url=url,
                          identity_file=identity_file)
        try:
            db_session.add(repo)
            current_user.generated_identity_file = None
            db_session.commit()
            result = 'ok'
        except Exception as e:
            logger.warning(e)
            db_session.rollback()
            result = 'fail'
            details = 'Failed to save the repository into database'
    else:
        result = 'fail'
        details = 'Failed to validate the url:<br> > {}'.format(
            validation['details'].replace('\n', '<br> > ')
        )

    return jsonify(dict(
        result=result,
        details=details,
        repositories=[dict(id=repo.id,
                           url=repo.url,
                           identity_file=repo.identity_file)
                      for repo in current_user.repositories]
    ))


def import_add_repository(app):
    @app.route('/api/repository/add')
    @login_required
    def add_repository():
        url = request.args['url']
        return _add_repository(url)

    @app.route('/api/repository/list')
    @login_required
    def repositories():
        return jsonify(dict(
            repositories=[dict(url=repo.url,
                               identity_file=repo.identity_file)
                          for repo in current_user.repositories]
        ))
