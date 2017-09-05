
class UIError(Exception):
    pass

class RepositoryError(UIError):
    pass


class MissingRepositoryId(RepositoryError):
    pass


class InvalidRepositoryId(RepositoryError):
    pass


class RepositoryNotFound(RepositoryError):
    pass


class RepositoryAccessDenied(RepositoryError):
    pass


class UserError(UIError):
    pass


class MissingUserId(UserError):
    pass


class InvalidUserId(UserError):
    pass
