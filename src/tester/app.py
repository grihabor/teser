import os
import subprocess
import tempfile
from urllib.parse import urlparse, ParseResult

from flask import Flask, request, jsonify

from util import DIR_ROOT, DIR_SRC

app = Flask(__name__)

WORKDIR = os.path.join(DIR_ROOT, 'workdir')
ARG_URL = 'url'
ARG_IDENTITY_FILE = 'identity_file'
DIR_TESTER = os.path.join(DIR_SRC, 'tester')
FILE_CLONE_SH = os.path.join(DIR_TESTER, 'clone.sh')

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
    if ARG_IDENTITY_FILE not in request.args:
        return jsonify(dict(details='identity_file_missing_error', ok=0))

    url = request.args[ARG_URL]
    parsed = parse_repo_url(url)

    if parsed is None:
        return jsonify(dict(ok=0, details='url_parsing_error'))

    identity_file_path = os.path.join('/keys', ARG_IDENTITY_FILE)

    with open(FILE_CLONE_SH, 'r') as template, \
            tempfile.NamedTemporaryFile('w') as f:
        content = template.read()
        content = content.format(identity_file=identity_file_path,
                                 **parsed)
        f.write(content)
        f.flush()

        command = ['sh', f.name]

        print('Command: {}'.format(' '.join(command)))

        if not os.path.exists(WORKDIR):
            os.mkdir(WORKDIR)

        with tempfile.NamedTemporaryFile('w') as f:
            completed = subprocess.run(command, cwd=WORKDIR, stdout=f.file, stderr=f.file)

            with open(f.name) as fr:
                out = fr.read()  # TODO Warning: maybe too large

    return jsonify(dict(ok=(completed.returncode == 0),
                        returncode=completed.returncode,
                        output=out))


def main():
    app.run('0.0.0.0', 6000, debug=True)


if '__main__' == __name__:
    main()
