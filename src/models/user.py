from flask_security import UserMixin
from sqlalchemy import (
    Boolean, DateTime, Column, Integer, String
)
from sqlalchemy.orm import relationship, backref

from database import Base


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))

    repositories = relationship('Repository')
    generated_identity_file = Column(String(255), nullable=True)

    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User id={0.id} email={0.email}>'.format(self)
