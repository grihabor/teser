from celery_app import app
import models 



@app.task(name='tasks.tests.run')
def run_tests(repo_id):
    repo = models.Repository.get(repo_id)
    kwargs = parse_repo_url(repo.url)
    if kwargs is None:
        return dict(
            result='fail',
            details='Invalid repository'
        )

    result = run_bash_script(
        FILE_TEST_SH,
        identity_file=repo.identity_file,
        git_template=Git(path='/grihabor/compressor',
                         user='git',
                         host='gitlab.com'),
        git=Git(**kwargs)
    )

    return dict(result)
    