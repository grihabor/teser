import functools
import logging
import os
import subprocess
import tempfile

from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap

from models import Repository
from util import DIR_SRC, DIR_KEYS, safe_get_repository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__, template_folder='../app/templates')
Bootstrap(app)

ARG_URL = 'url'
ARG_IDENTITY_FILE = 'identity_file'
ARG_REPOSITORY_ID = 'repository_id'


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


def inside_tempdir(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        with tempfile.TemporaryDirectory() as tempdir:
            return f(*args, tempdir=tempdir, **kwargs)

    return wrapper


@inside_tempdir
def run_bash_script(template_path, *, git, identity_file, tempdir):
    identity_file_path = os.path.join(DIR_KEYS, identity_file)

    with open(template_path, 'r') as template, \
            tempfile.NamedTemporaryFile('w') as f:
        content = template.read()
        content = content.format(
            identity_file_path=identity_file_path,
            identity_file=identity_file,
            repository_name=git.path.rsplit('/', 1)[-1],
            git=git
        )
        f.write(content)
        f.flush()

        command = ['sh', f.name]

        print('Command: {}'.format(' '.join(command)))

        with tempfile.NamedTemporaryFile('w') as f:
            process = subprocess.Popen(command, cwd=tempdir, stdout=f.file, stderr=f.file)
            try:
                process.communicate(timeout=100)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()

            with open(f.name) as fr:
                out = fr.read()  # TODO Warning: maybe too large

    return dict(ok=(process.returncode == 0),
                returncode=process.returncode,
                details=out)


@app.route('/run_tests')
def run_tests():
    repo = safe_get_repository(ARG_REPOSITORY_ID)  # type: Repository

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
