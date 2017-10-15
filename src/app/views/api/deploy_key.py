import logging
import os
import subprocess
import uuid

from flask import jsonify
from flask_security import login_required, current_user

from database import db_session
from utils import DIR_KEYS
from tasks import generate_deploy_key

logger = logging.getLogger(__name__)


def import_generate_deploy_key(app):
    @app.route('/api/deploy_key/generate', methods=['GET'])
    @login_required
    def generate_deploy_key_endpoint():
        result = generate_deploy_key.delay(current_user.id)
        logger.info('Waiting for deploy key to generate...')
        deploy_key = result.get()
        return jsonify(dict(deploy_key=deploy_key, result='ok'))
        
        