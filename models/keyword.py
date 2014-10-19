from sqlalchemy import Column, Integer, String

from base import Base


class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)
    keyword = Column(String)
    phonetic_code = Column(String(5))