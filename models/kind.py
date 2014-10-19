from sqlalchemy import Column, Integer, String

from base import Base


class Kind(Base):
    __tablename__ = 'kind_type'

    id = Column(Integer, primary_key=True)
    kind = Column(String(15))