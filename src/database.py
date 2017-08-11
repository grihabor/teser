import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

POSTGRES_PASSWORD = 'POSTGRES_PASSWORD'
POSTGRES_USER = 'POSTGRES_USER'
POSTGRES_DB = 'POSTGRES_DB'
POSTGRES_HOST = 'POSTGRES_HOST'

engine = create_engine(
    'postgresql://{user}:{password}@{host}/{db_name}'.format(
        user=os.getenv(POSTGRES_USER),
        password=os.getenv(POSTGRES_PASSWORD),
        host=os.getenv(POSTGRES_HOST),
        db_name=os.getenv(POSTGRES_DB)
    ),
    convert_unicode=True
)

db_session = scoped_session(
    sessionmaker(autocommit=False,
                 autoflush=False,
                 bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
