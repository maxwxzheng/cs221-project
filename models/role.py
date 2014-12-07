from sqlalchemy import Column, Integer, String

from base import Base


ACTOR = 1
ACTRESS = 2
PRODUCER = 3
DIRECTOR = 8


class Role(Base):
    __tablename__ = 'role_type'

    id = Column(Integer, primary_key=True)
    role = Column(String(32))