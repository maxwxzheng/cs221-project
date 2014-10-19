from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

class Movie(Base):
    __tablename__ = 'title'

    id = Column(Integer, primary_key=True)

    title = Column(String(65535))
    imdb_index = Column(String(12))

    kind_id = Column(Integer, ForeignKey('kind_type.id'))
    kind = relationship("Kind", backref=backref('movies'))

    production_year = Column(Integer)
    imdb_id = Column(Integer)
    phonetic_code = Column(String)

    episode_of_id = Column(Integer)
    season_nr = Column(Integer)
    episode_nr = Column(Integer)

    series_years = Column(String)

    md5sum = Column(String(32))

    keywords = association_proxy('movie_keywords', 'keyword')
    people = association_proxy('cast_info', 'person')