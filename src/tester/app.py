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
    o = urlparse(url)  # type: ParseResult

    attrs = [
        'scheme',
        'netloc',
        'path',
        'params',
        'query',
        'fragment',
        'username',
        'password',
        'hostname',
        'port',
    ]

    return {attr: getattr(o, attr, None) for attr in attrs}


@app.route('/clone_repo')
def clone_repo():
    if ARG_URL not in request.args:
        return jsonify(dict(details='missing_url', ok=0))

    url = request.args[ARG_URL]
    parsed = parse_repo_url(url)

    if parsed['hostname'] is None:
        return jsonify(dict(ok=0, details='missing_hostname', parsed=parsed))

    command = ['git',
               'clone',
               '{username}@{hostname}:{path}'.format(**parsed)]

    print('Command: {}'.format(' '.join(command)))

    completed = subprocess.run(command, cwd=WORKDIR)
    return jsonify(dict(ok=(completed.returncode == 0),
                        returncode=completed.returncode))


def main():
    app.run('0.0.0.0', 6000, debug=True)


if '__main__' == __name__:
    main()
