from sqlalchemy import Column, Integer, String

from base import Base


class Character(Base):
    __tablename__ = 'char_name'

    id = Column(Integer, primary_key=True)

    name = Column(String(65535))

    imdb_index = Column(String(12))
    imdb_id = Column(Integer)

    name_pcode_nf = Column(String(5))
    surname_pcode = Column(String(5))

    md5sum = Column(String(32))