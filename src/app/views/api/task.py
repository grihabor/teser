import logging

import urllib

import json
from flask import jsonify
from flask_security import login_required\

from util import safe_get_repository
from util.unified_response import UnifiedResponse


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def import_task(app):
    @app.route('/api/task/start')
    @login_required
    def task_start():
        repo = safe_get_repository('repository_id')

        url = f'http://tester:6000/run_tests?repository_id={repo.id}&user_id={repo.user_id}'
        with urllib.request.urlopen(url) as f:
            response = f.read()

        return response
