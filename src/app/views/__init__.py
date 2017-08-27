from .deploy_key import import_generate_deploy_key
from .repository import import_add_repository
from .index import import_index
from .home import import_home


def import_views(app):
    import_generate_deploy_key(app)
    import_add_repository(app)
    import_index(app)
    import_home(app)
