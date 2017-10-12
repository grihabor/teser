import os
import logging
from sqlalchemy.exc import SQLAlchemyError
from datastore import user_datastore

logger = logging.getLogger(__name__)


def create_admins():
    admins = os.getenv('ADMINS', None)
    if not admins:
        return

    logger.info(f'Creating admins: {admins}')

    try:
        admin_role = user_datastore.find_or_create_role('admin')
        for admin_email in admins.split(','):
            admin = user_datastore.get_user(admin_email)
            if admin:
                user_datastore.add_role_to_user(admin, admin_role)
        user_datastore.commit()
    except SQLAlchemyError as e:
        logger.warning(f'Failed to initialize admins: {e}')
