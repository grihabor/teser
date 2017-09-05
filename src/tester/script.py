import subprocess
import os
import tempfile
import functools

import logging

from util import DIR_KEYS

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


@inside_tempdir
def run_bash_script(template_path, *, tempdir, **kwargs):
    output_list = []
    returncode = 0
    identity_file_path = os.path.join(DIR_KEYS, kwargs['identity_file'])

    with open(template_path, 'r') as template:
        content_template = template.read()
        content = content_template.format(
            identity_file_path=identity_file_path,
            repository_name=kwargs['git'].path.rsplit('/', 1)[-1],
            **kwargs
        )

        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('#') or line == '':
                continue

            command = line.split()
            logger.info('Command: {}'.format(command))
            result = run_command(command, tempdir)
            output_list.append(result.output)
            if result.returncode != 0:
                returncode = result.returncode
                break

    return dict(ok=(returncode == 0),
                returncode=returncode,
                details=output_list)
