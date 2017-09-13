import subprocess
import os
import tempfile
import functools

import logging

from util import DIR_KEYS
from util.unified_response import UnifiedResponse

logger = logging.getLogger(__name__)


def inside_tempdir(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        with tempfile.TemporaryDirectory() as tempdir:
            return f(*args, tempdir=tempdir, **kwargs)

    return wrapper


def run_command(command, tempdir, timeout=10):
    with tempfile.NamedTemporaryFile('w') as f:
        process = subprocess.Popen(
            command,
            cwd=tempdir,
            stdout=f.file,
            stderr=f.file
        )
        try:
            process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as e:
            process.kill()
            process.communicate()
            f.file.write('\n'.join([
                '',
                '',
                'Timeout ({}s): {}'.format(timeout, command)
            ]))

        with open(f.name) as fr:
            output = fr.read()  # TODO Warning: maybe too large

    return Result(output, process.returncode)


class Result:
    def __init__(self, output, returncode):
        self.output = output
        self.returncode = returncode


def preprocess_script(f, **kwargs):
    script_code = []

    check_code = '\n'.join([
        'if [ $? -eq 0 ]; then',
        '    echo "-- ok: {command}"',
        'else',
        '    echo "-- fail: {command}"',
        '    exit 1',
        'fi',
    ])

    for raw_line in f:
        line = raw_line.strip()
        logger.info(line)
        if line == '':
            continue
        command = line.format(**kwargs)
        script_code.append(command)
        script_code.append(check_code.format(command=command))

    return '\n'.join(script_code)


@inside_tempdir
def run_bash_script(template_path, *, tempdir, **kwargs):
    logger.info('Run script: {}'.format(template_path))
    identity_file_path = os.path.join(DIR_KEYS, kwargs['identity_file'])

    with open(template_path, 'r') as template, \
            tempfile.NamedTemporaryFile('w') as f:
        values = dict(
            identity_file_path=identity_file_path,
            repository_name=kwargs['git'].path.rsplit('/', 1)[-1],
            **kwargs
        )
        content = preprocess_script(template, **values)
        f.write(content)
        f.flush()

        command = ['sh', f.name]

        logger.info('Command: {}'.format(' '.join(command)))

        with tempfile.NamedTemporaryFile('w') as f:
            process = subprocess.Popen(command, cwd=tempdir, stdout=f.file, stderr=f.file)
            try:
                process.communicate(timeout=100)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()

            with open(f.name) as fr:
                output = fr.read()  # TODO Warning: maybe too large

    return UnifiedResponse(
        result='ok' if (process.returncode == 0) else 'fail',
        details=output.split('\n')
    )
