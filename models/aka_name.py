from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base


class AkaName(Base):
    __tablename__ = 'aka_name'

    id = Column(Integer, primary_key=True)

    person_id = Column(Integer, ForeignKey('name.id'))
    person = relationship("Person", backref=backref('aka_names'))

    name = Column(String(65535))
    imdb_index = Column(String(12))

    name_pcode_cf = Column(String(5))
    name_pcode_nf = Column(String(5))
    surname_pcode = Column(String(5))

    md5sum = Column(String(32))