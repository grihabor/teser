import logging
import urllib

from flask import jsonify, json
from flask_security import login_required

from tasks import run_tests
from utils import safe_get_repository

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

        task_result = run_tests.delay(repo.id)
        logger.info('Waiting for run_tests...')
        return jsonify(result='ok', details='logs not implemented'), 501

        result = task_result.get()
        logger.info(f'Got: {result}')
        result['details'] = [
            dict(text=text,
                 color=color_mapping(text))
            for text in result['details']
        ]
        return jsonify(result)
