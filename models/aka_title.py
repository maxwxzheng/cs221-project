from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base


class AkaTitle(Base):
    __tablename__ = 'aka_title'

    id = Column(Integer, primary_key=True)

    movie_id = Column(Integer, ForeignKey('title.id'))
    movie = relationship("Movie", backref=backref('aka_titles'))

    kind_id = Column(Integer, ForeignKey('kind_type.id'))
    kind = relationship("Kind", backref=backref('aka_titles'))

    title = Column(String)
    imdb_index = Column(String(12))
    production_year = Column(Integer)
    phonetic_code = Column(String)

    episode_of_id = Column(Integer)
    season_nr = Column(Integer)
    episode_nr = Column(Integer)

    note = Column(String)

    md5sum = Column(String(32))