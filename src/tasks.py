from celery_app import app
from models import Repository



class Git:
    def __init__(self, user, host, path):
        self.path = path
        self.user = user
        self.host = host
        
        
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
    return Git(user=user,
               host=host,
               path=path)

@app.task(name='tasks.tests.run')
def run_tests(repo_id):
    repo = Repository.get(repo_id)
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
    