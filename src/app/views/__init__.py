from views.admin_page import import_admin_page
from views.user import import_user
from .deploy_key import import_generate_deploy_key
from .repository import import_repository
from .index import import_index
from .home import import_home


def import_views(app):
    import_generate_deploy_key(app)
    import_repository(app)
    import_index(app)
    import_home(app)
    import_admin_page(app)
    import_user(app)

