from flask_security import RoleMixin
from sqlalchemy import (
    Column, Integer,
    String
)

from database import Base


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __repr__(self):
        return '<Role id={0.id} name={0.name}>'.format(self)
