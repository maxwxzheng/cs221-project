from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class Kind(Base):
    __tablename__ = 'kind_type'

    id = Column(Integer, primary_key=True)
    kind = Column(String(15))