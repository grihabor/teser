import os

from . import app
from models import Repository
from tester.script import run_bash_script
from utils import DIR_SRC, parse_repo_url, UnifiedResponse

DIR_TASKS = os.path.join(DIR_SRC, 'tasks')
FILE_CLONE_SH = os.path.join(DIR_TASKS, 'clone.sh')
FILE_TEST_SH = os.path.join(DIR_TASKS, 'test.sh')


def missing(arg):
    return 'Missing argument: {}'.format(arg)


@app.task(name='tasks.repository.clone')
def clone_repository(url, identity_file, user_email):
    repo_location = parse_repo_url(url)

    if repo_location is None:
        return UnifiedResponse(
            result='fail',
            details='URL parsing error'
        )

    result = run_bash_script(
        FILE_CLONE_SH,
        user_email,
        identity_file=identity_file,
        git=repo_location,
    )

    return result

