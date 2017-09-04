import os

from flask import request
from flask_security import current_user

from models import Repository

DIR_UTIL = os.path.split(os.path.abspath(__file__))[0]
DIR_SRC = os.path.normpath(os.path.join(DIR_UTIL, os.pardir))
DIR_ROOT = os.path.normpath(os.path.join(DIR_SRC, os.pardir))

DIR_KEYS = os.path.join(DIR_ROOT, 'keys')


class RepositoryError(Exception):
    pass


class MissingRepositoryId(RepositoryError):
    pass


class InvalidRepositoryId(RepositoryError):
    pass


class RepositoryNotFound(RepositoryError):
    pass


class RepositoryAccessDenied(RepositoryError):
    pass


def safe_get_repository(id_arg):
    if id_arg not in request.args:
        raise MissingRepositoryId(id_arg)

    repo_id = request.args[id_arg]
    try:
        repo_id = int(repo_id)
    except ValueError:
        raise InvalidRepositoryId('Failed to convert {} to {}'.format(repo_id, int))

    repo = Repository.query.get(repo_id)

    if repo is None:
        raise RepositoryNotFound(str(repo_id))

    if repo.user_id != current_user.id:
        raise RepositoryAccessDenied('User does not own the repository')

    return repo
