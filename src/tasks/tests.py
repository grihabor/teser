from celery_app import app
from models import Repository
from tasks.repository import FILE_TEST_SH

from tester.script import run_bash_script
from utils import parse_repo_url, RepositoryLocation


@app.task(name='tasks.tests.run')
def run_tests(repo_id):
    repo = Repository.query.get(repo_id)
    git_obj = parse_repo_url(repo.url)
    if git_obj is None:
        return dict(
            result='fail',
            details='Invalid repository'
        )

    result = run_bash_script(
        FILE_TEST_SH,
        identity_file=repo.identity_file,
        git_template=RepositoryLocation(path='/grihabor/compressor',
                                        user='git',
                                        host='gitlab.com'),
        git=git_obj
    )

    return dict(result)
