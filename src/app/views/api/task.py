import logging
import urllib

from flask import jsonify, json
from flask_security import login_required

from util import safe_get_repository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def color_mapping(text: str):
    if text.startswith('-- ok:'):
        return 'green'
    if text.startswith('-- fail:'):
        return 'red'
    return 'black'


def import_task(app):
    @app.route('/api/task/start')
    @login_required
    def task_start():
        repo = safe_get_repository('repository_id')

        url = f'http://tester:6000/run_tests?repository_id={repo.id}&user_id={repo.user_id}'
        with urllib.request.urlopen(url) as f:
            response = f.read()

        result = json.loads(response)
        result['details'] = [
            dict(text=text,
                 color=color_mapping(text))
            for text in result['details']
        ]
        return jsonify(result)
