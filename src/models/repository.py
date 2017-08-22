from database import Base
from sqlalchemy import (
    Integer, String, ForeignKey, Column
)


class Repository(Base):
    __tablename__ = 'repository'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    url = Column(String(2000), nullable=False)  # https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers
    identity_file = Column(String(255))
