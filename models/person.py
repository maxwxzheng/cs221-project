from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class Person(Base):
    __tablename__ = 'name'

    id = Column(Integer, primary_key=True)

    name = Column(String(65535))
    imdb_index = Column(String(12))
    imdb_id = Column(Integer)
    gender = Column(String(1))

    name_pcode_cf = Column(String(5))
    name_pcode_nf = Column(String(5))
    surname_pcode = Column(String(5))

    md5sum = Column(String(32))