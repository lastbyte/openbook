
from enum import Enum
from sqlalchemy import Boolean, Column, Integer, String

from db.database import Base

USER_ROLE = Enum('USER_ROLE', ['ADMIN', 'USER'])


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default=USER_ROLE.USER.name)
    active = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"User(email={self.email}, active={self.active})"
