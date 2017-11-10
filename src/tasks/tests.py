import os
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
        
    template_location = RepositoryLocation(
        path='Ploshkin/compressor.git',
        user='git',
        host='gitlab.com',
    )

    result = run_bash_script(
        FILE_TEST_SH,
        repo.user.email,
        identity_file=repo.identity_file,
        git_template=template_location,
        git=git_obj,
        save_results=True,
    )

    return dict(result)
