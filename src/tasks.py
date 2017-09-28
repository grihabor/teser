from celery_app import app
from util import parse_repo_url


@app.task(name='tasks.tests.run')
def tests_run(repo_id):
    repo = Repository.get(repo_id)
    kwargs = parse_repo_url(repo.url)
    if kwargs is None:
        return dict(UnifiedResponse(
            result='fail',
            details='Invalid repository'
        ))

    result = run_bash_script(
        FILE_TEST_SH,
        identity_file=repo.identity_file,
        git_template=Git(path='/grihabor/compressor',
                         user='git',
                         host='gitlab.com'),
        git=Git(**kwargs)
    )

    if 'debug' in request.args:
        result.details = process_details(result.details)
        return render_template('debug.html', **dict(result))

    return jsonify(dict(result))