import json
import logging
import urllib

from flask import request, jsonify
from flask_security import login_required, current_user, roles_required

from database import db_session
from models import Repository, User
from util import safe_get_repository
from util.details import process_details
from util.exception import UIError
from util.unified_response import UnifiedResponse

from sqlalchemy.orm import join

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def import_task(app):
    @app.route('/api/task/start')
    @login_required
    def task_start():
        repo = safe_get_repository('repository_id')
        r = UnifiedResponse(result='fail', details='Not implemented')
        return jsonify(dict(r))

