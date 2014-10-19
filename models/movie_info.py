from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base


"""MovieInfo contains everything but
'bottom 10 rank', 'rating', 'top 250 rank',
'votes', and 'votes distribution'.

MovieInfoIDX contains only those.
"""


class MovieInfo(Base):
    __tablename__ = 'movie_info'

    id = Column(Integer, primary_key=True)

    movie_id = Column(Integer, ForeignKey('title.id'))
    movie = relationship("Movie", backref=backref('movie_info'))

    info_type_id = Column(Integer, ForeignKey('info_type.id'))
    info_type = relationship("InfoType", backref=backref('movie_info'))

    info = Column(String)
    note = Column(String)


class MovieInfoIDX(Base):
    __tablename__ = 'movie_info_idx'

    id = Column(Integer, primary_key=True)

    movie_id = Column(Integer, ForeignKey('title.id'))
    movie = relationship("Movie", backref=backref('movie_info_idx'))

    info_type_id = Column(Integer, ForeignKey('info_type.id'))
    info_type = relationship("InfoType", backref=backref('movie_info_idx'))

    info = Column(String)
    note = Column(String)