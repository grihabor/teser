from sqlalchemy import (
    Integer, String, ForeignKey, Column
)
from sqlalchemy.orm import relationship

from database import Base


class Repository(Base):
    __tablename__ = 'repository'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='repositories', foreign_keys=[user_id])
    
    url = Column(String(2000), nullable=False)  # https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers
    identity_file = Column(String(255), nullable=False)

    def __iter__(self):
        return list(dict(
            url=self.url,
            identity_file=self.identity_file,
            id=self.id,
        ).items())
