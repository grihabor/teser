import json
import logging
import urllib

from flask import request, jsonify
from flask_security import login_required, current_user

from database import db_session
from models import Repository

logger = logging.getLogger(__name__)


def validate_repository(url, identity_file):
    path = 'http://tester/clone_repo?url={}&identity_file={}'.format(
        url, identity_file
    )

    with urllib.request.urlopen(path) as r:
        content = r.read()
        logger.info(content)
        obj = json.loads(content)
    return obj.ok


def import_add_repository(app):
    @app.route('/add_repository')
    @login_required
    def add_repository():
        url = request.args['url']
        identity_file = current_user.generated_identity_file

        if identity_file is None:
            return "", 500

        if validate_repository(url, identity_file):
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
                result = 'invalid repository'
        else:
            result = 'invalid repository'

        return jsonify(dict(
            result=result,
            repositories=[dict(url=repo.url)
                          for repo in current_user.repositories]
        ))
