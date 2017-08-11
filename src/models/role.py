from database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy import (
    Boolean, DateTime, Column, Integer,
    String, ForeignKey
)




class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
