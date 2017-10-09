from .admin_page import import_admin_page
from .api import import_api
from .home import import_home
from .index import import_index


def import_views(app):
    # actual views
    import_index(app)
    import_home(app)
    import_admin_page(app)
    # api
    import_api(app)
