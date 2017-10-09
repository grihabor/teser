from flask_security import SQLAlchemySessionUserDatastore
from database import db_session
from models import User, Role


user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)

