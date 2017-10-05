import logging
import socket

from utils.repository import RepositoryLocation

logging.basicConfig(level=logging.INFO)

import os

from flask import Flask, request, jsonify
from flask_bootstrap import Bootstrap

from tester.script import run_bash_script
from utils import (
    DIR_SRC,
    UnifiedResponse,
    parse_repo_url)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__, template_folder='../app/templates')
Bootstrap(app)

ARG_URL = 'url'
ARG_IDENTITY_FILE = 'identity_file'
ARG_REPOSITORY_ID = 'repository_id'
ARG_USER_ID = 'user_id'


@app.route('/')
def index():
    return 'Internal tester service'



def routes():
    routes = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return routes






@app.route('/clone_repo', methods=['GET'])
def clone_repo():
    return jsonify(dict(_clone_repo()))


def main():
    logger.info('Starting tester...')
    app.run('0.0.0.0', 6000, debug=True)


if '__main__' == __name__:
    main()
