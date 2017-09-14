from celery_app import app


@app.task
def run_tests(repo_id, user_id):
    url = f'http://tester:6000/run_tests?repository_id={repo_id}&user_id={user_id}'
    with urllib.request.urlopen(url) as f:
        response = f.read()
    return response
    