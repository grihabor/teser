import os
import subprocess
from urllib.parse import urlparse, ParseResult

from flask import Flask, request, jsonify

from util import DIR_ROOT

app = Flask(__name__)

WORKDIR = os.path.join(DIR_ROOT, 'workdir')
ARG_URL = 'url'


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


@app.route('/clone_repo')
def clone_repo():
    if ARG_URL not in request.args:
        return jsonify(dict(details='url_missing_error', ok=0))

    url = request.args[ARG_URL]
    parsed = parse_repo_url(url)

    if parsed is None:
        return jsonify(dict(ok=0, details='url_parsing_error'))

    command = ['git',
               'clone',
               '{user}@{host}:{path}'.format(**parsed)]

    print('Command: {}'.format(' '.join(command)))

    completed = subprocess.run(command, cwd=WORKDIR)
    return jsonify(dict(ok=(completed.returncode == 0),
                        returncode=completed.returncode))


def main():
    app.run('0.0.0.0', 6000, debug=True)


if '__main__' == __name__:
    main()
