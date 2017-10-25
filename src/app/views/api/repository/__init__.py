from .activation import import_repository_activate
from .new_repo import import_repository_add
from .removal import import_repository_remove
from .repo_list import import_repository_list, user_repositories


def import_repository(app):
    import_repository_add(app)
    import_repository_list(app)
    import_repository_activate(app)
    import_repository_remove(app)
