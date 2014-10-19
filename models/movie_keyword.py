from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class MovieKeyword(Base):
    __tablename__ = 'movie_keyword'

    id = Column(Integer, primary_key=True)

    movie_id = Column(Integer, ForeignKey('title.id'))
    movie = relationship("Movie", backref=backref('movie_keywords'))

    keyword_id = Column(Integer, ForeignKey('keyword.id'))
    keyword = relationship("Keyword", backref=backref('movie_keywords'))