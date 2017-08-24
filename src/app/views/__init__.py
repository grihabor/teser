from .deploy_key import import_generate_deploy_key
from .view_add_repository import import_add_repository


def import_views(app):
    import_generate_deploy_key(app)
    import_add_repository(app)
