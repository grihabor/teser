from flas_security import SQLAlchemySessionUserDatastore

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)

