import logging
import os
import shutil
import subprocess
import sys
from time import sleep

from sqlalchemy.exc import SQLAlchemyError

from database import POSTGRES_URL, Base, db_session
from utils import DIR_SRC
from .admins import create_admins

DIR_APP = os.path.join(DIR_SRC, 'app')
DIR_TEMPLATES = os.path.join(DIR_APP, 'templates')
FILE_BASE_HTML = os.path.join(DIR_TEMPLATES, 'base.html')
FILE_BASE_HTML_EXAMPLE = FILE_BASE_HTML + '.example'

FILE_ALEMBIC_INI = os.path.join(DIR_SRC, 'alembic.ini')
FILE_ALEMBIC_INI_EXAMPLE = FILE_ALEMBIC_INI + '.example'

SQLALCHEMY_URL = 'sqlalchemy.url'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def maybe_create_base_html():
    if not os.path.exists(FILE_BASE_HTML):
        shutil.copy(FILE_BASE_HTML_EXAMPLE, FILE_BASE_HTML)
        logger.info(f'cp {FILE_BASE_HTML_EXAMPLE} {FILE_BASE_HTML}')
    else:
        logger.info(f'File {FILE_BASE_HTML} exists')


def maybe_create_alembic_ini():
    if not os.path.exists(FILE_ALEMBIC_INI):
        with open(FILE_ALEMBIC_INI_EXAMPLE, 'r') as example, \
                open(FILE_ALEMBIC_INI, 'w') as ini:
            for line in example:
                if SQLALCHEMY_URL not in line:
                    ini.write(line)
                else:
                    ini.write('{} = {}\n'.format(
                        SQLALCHEMY_URL, POSTGRES_URL
                    ))


def run_migrations():
    subprocess.run(["alembic", "upgrade", "head"],
                   cwd=DIR_SRC,
                   stdout=sys.stdout,
                   stderr=subprocess.STDOUT)


def _init():
    Base.metadata.create_all()
    maybe_create_base_html()
    maybe_create_alembic_ini()
    run_migrations()


def init():
    while True:
        try:
            _init()
            db_session.commit()
            return
        except SQLAlchemyError as e:
            db_session.rollback()
            logger.info(str(e))
        sleep(.5)