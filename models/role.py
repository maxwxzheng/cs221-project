from sqlalchemy import Column, Integer, String

from base import Base


class Role(Base):
    __tablename__ = 'role_type'

    id = Column(Integer, primary_key=True)
    role = Column(String(32))