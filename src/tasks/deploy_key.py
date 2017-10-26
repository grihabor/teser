from celery.utils.log import get_task_logger
import os
import subprocess
import uuid

from celery_app import app
from database import db_session
from models import User
from sqlalchemy.exc import SQLAlchemyError
from utils import DIR_KEYS

logger = get_task_logger(__name__)


def get_key_path(identity_file):
    return os.path.join(DIR_KEYS, identity_file)


def generate_new_key_pair():
    identity_file = str(uuid.uuid4())
    path = get_key_path(identity_file)
    subprocess.run(['ssh-keygen',
                            '-q',
                            '-t', 'rsa',
                            '-b', '2048',
                            '-f', path,
                            '-N', '', ])
    logger.info(f'Generate new key pair: {identity_file}')
    return identity_file
        

def key_exists(identity_file):
    
    if identity_file is None:
        return False
        
    path = get_key_path(identity_file)
    public_key = path + '.pub'
    return os.path.exists(path) and os.path.exists(public_key)
    

def maybe_generate_new_key_pair(current_user):
    identity_file = current_user.generated_identity_file

    if not key_exists(identity_file):
        identity_file = generate_new_key_pair()
        try:
            current_user.generated_identity_file = identity_file
            db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            raise
            
    return identity_file


@app.task(name='tasks.deploy_key.generate')
def generate_deploy_key(user_id):
    current_user = User.query.get(user_id)
    identity_file = maybe_generate_new_key_pair(current_user)
    
    path = get_key_path(identity_file)
    
    with open(f'{path}.pub', 'r') as f:
        public_key = f.read()

    return public_key
