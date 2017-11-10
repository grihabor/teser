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
        
    results_dir = os.path.join(
        os.environ['VOLUME_RESULTS'], 
        user_email, 
        identity_file, 
        commit_hash,
    )
    os.makedirs(results_dir, exist_ok=True)
    results_path = os.path.join(results_dir, 'results.csv')

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
        results_path=results_path
    )

    return dict(result)
