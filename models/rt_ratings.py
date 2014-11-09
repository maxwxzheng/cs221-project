from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from base import Base


class RtRatings(Base):
    __tablename__ = 'rt_ratings'

    imdb_movie_id = Column(Integer, primary_key=True)
    rt_movie_id = Column(Integer)
    critics_score = Column(Integer)
    critics_rating = Column(String(20))
    audience_score = Column(Integer)
    audience_rating = Column(String(20))
    rt_title = Column(String(85))
