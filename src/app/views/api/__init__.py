from .deploy_key import import_generate_deploy_key
from .repository import import_repository
from .task import import_task
from .user import import_user


def import_api(app):
    import_task(app)
    import_generate_deploy_key(app)
    import_user(app)
    import_repository(app)
