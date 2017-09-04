from flask_bootstrap import Bootstrap
import os
import subprocess
import tempfile

import logging
from flask import Flask, request, jsonify, render_template

from util import DIR_ROOT, DIR_SRC, DIR_KEYS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__, template_folder='../app/templates')
Bootstrap(app)

WORKDIR = os.path.join(DIR_ROOT, 'workdir')
ARG_URL = 'url'
ARG_IDENTITY_FILE = 'identity_file'
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


@app.route('/clone_repo', methods=['GET'])
def clone_repo():
    if ARG_URL not in request.args:
        return jsonify(dict(details='url_missing_error', ok=0))
    if ARG_IDENTITY_FILE not in request.args:
        return jsonify(dict(details='identity_file_missing_error', ok=0))

    url = request.args[ARG_URL]
    parsed = parse_repo_url(url)
    identity_file = request.args[ARG_IDENTITY_FILE]

    if parsed is None:
        return jsonify(dict(ok=0, details='url_parsing_error'))

    return jsonify(run_bash_script(
        FILE_CLONE_SH,
        identity_file=identity_file,
        **parsed
    ))


def run_bash_script(template_path, *, path, user, host, identity_file):
    identity_file_path = os.path.join(DIR_KEYS, identity_file)

    with open(template_path, 'r') as template, \
            tempfile.NamedTemporaryFile('w') as f:
        content = template.read()
        content = content.format(
            identity_file=identity_file_path,
            repository_name=path.rsplit('/', 1)[-1],
            path=path,
            user=user,
            host=host,
        )
        f.write(content)
        f.flush()

        command = ['sh', f.name]

        print('Command: {}'.format(' '.join(command)))

        if not os.path.exists(WORKDIR):
            os.mkdir(WORKDIR)

        with tempfile.NamedTemporaryFile('w') as f:
            process = subprocess.Popen(command, cwd=WORKDIR, stdout=f.file, stderr=f.file)
            try:
                process.communicate(timeout=10)
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
    # repo_id = int(request.args['repository_id'])
    json_data = run_bash_script(
        FILE_TEST_SH,
        identity_file='8ad998dd-4c89-404d-94b5-e2f99c3c5700',
        path='/grihabor/compressor',
        user='git',
        host='gitlab.com',
    )

    if not request.remote_addr.startswith('172.'):
        return render_template('debug.html', **json_data)

    return jsonify(json_data)


def main():
    logger.info('Starting tester...')
    app.run('0.0.0.0', 6000, debug=True)


if '__main__' == __name__:
    main()
