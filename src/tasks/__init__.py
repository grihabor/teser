from celery_app import app

from .tests import run_tests
from .repository import clone_repository
from .deploy_key import generate_deploy_key