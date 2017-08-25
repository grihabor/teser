import logging
import os
import subprocess
import uuid

from flask import jsonify
from flask_security import login_required, current_user

from database import db_session
from util import DIR_KEYS

logger = logging.getLogger(__name__)


def import_generate_deploy_key(app):
    @app.route('/generate_deploy_key', methods=['GET'])
    @login_required
    def generate_deploy_key():
        identity_file = current_user.generated_identity_file

        if identity_file is None:
            identity_file = str(uuid.uuid4())
            path = os.path.join(DIR_KEYS, identity_file)
            subprocess.run(['ssh-keygen',
                            '-q',
                            '-t', 'rsa',
                            '-b', '2048',
                            '-f', path,
                            '-N', '', ])
            logger.info('Generated: {}'.format(identity_file))

            try:
                current_user.generated_identity_file = identity_file
                db_session.commit()
            except Exception as e:
                logger.warning(e)
                db_session.rollback()
        else:
            path = os.path.join(DIR_KEYS, identity_file)
            logger.info('Use saved one: {}'.format(identity_file))

        public_key = path + '.pub'
        if not os.path.exists(public_key):
            logger.info("Saved key doesn't exist: {}".format(public_key))
            try:
                current_user.generated_identity_file = None
                db_session.commit()
            except Exception as e:
                logger.warning(e)
                db_session.rollback()
            return generate_deploy_key()

        with open(public_key, 'r') as f:
            public_key = f.read()

        return jsonify(dict(result='ok', deploy_key=public_key))
