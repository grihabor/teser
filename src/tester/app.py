import logging
logging.basicConfig(level=logging.INFO)

import os

from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap

from models import Repository
from tester.script import run_bash_script
from util import DIR_SRC, safe_get_repository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__, template_folder='../app/templates')
Bootstrap(app)

ARG_URL = 'url'
ARG_IDENTITY_FILE = 'identity_file'
ARG_REPOSITORY_ID = 'repository_id'
ARG_USER_ID = 'user_id'

DIR_TESTER = os.path.join(DIR_SRC, 'tester')
FILE_CLONE_SH = os.path.join(DIR_TESTER, 'clone.sh')
FILE_TEST_SH = os.path.join(DIR_TESTER, 'test.sh')


@app.route('/')
def index():
    return 'Internal tester service'


def parse_repo_url(url):
    """Format: {user}@{host}:{path}"""

    result = url.split(':')
    if len(result) != 2:
        return

    hostinfo, path = result
    result = hostinfo.split('@')
    if len(result) != 2:
        return

    user, host = result
    return dict(user=user,
                host=host,
                path=path)


def routes():
    routes = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return routes


class Git:
    def __init__(self, user, host, path):
        self.path = path
        self.user = user
        self.host = host


def missing(arg):
    return 'Missing argument: {}'.format(arg)


@app.route('/clone_repo', methods=['GET'])
def clone_repo():
    if ARG_URL not in request.args:
        return jsonify(dict(details=missing(ARG_URL), ok=0))
    if ARG_IDENTITY_FILE not in request.args:
        return jsonify(dict(details=missing(ARG_IDENTITY_FILE), ok=0))

    url = request.args[ARG_URL]
    parsed = parse_repo_url(url)
    identity_file = request.args[ARG_IDENTITY_FILE]

    if parsed is None:
        return jsonify(dict(ok=0, details='URL parsing error'))

    return jsonify(run_bash_script(
        FILE_CLONE_SH,
        identity_file=identity_file,
        git=Git(**parsed)
    ))


@app.route('/run_tests')
def run_tests():
    repo = safe_get_repository(ARG_REPOSITORY_ID, ARG_USER_ID)  # type: Repository

    json_data = run_bash_script(
        FILE_TEST_SH,
        identity_file='349f4e08-4476-4aa0-a724-49946d52d684',
        git_template=Git(path='/grihabor/compressor',
                         user='git',
                         host='gitlab.com'),
        git=Git(**parse_repo_url(repo.url))
    )

    logger.info('Client address: {}'.format(request.remote_addr))

    if request.remote_addr.endswith('.0.1'):
        return render_template('debug.html', **json_data)

    return jsonify(json_data)


def main():
    logger.info('Starting tester...')
    app.run('0.0.0.0', 6000, debug=True)


if '__main__' == __name__:
    main()
