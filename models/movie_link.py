from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base


class MovieLink(Base):
    __tablename__ = 'movie_link'

    id = Column(Integer, primary_key=True)

    movie_id = Column(Integer, ForeignKey('title.id'))
    movie = relationship("Movie", foreign_keys='MovieLink.movie_id', backref=backref('linked_movies'))

    linked_movie_id = Column(Integer, ForeignKey('title.id'))
    linked_movie = relationship("Movie", foreign_keys='MovieLink.linked_movie_id')

    link_type_id = Column(Integer, ForeignKey('link_type.id'))
    link_type = relationship("LinkType", backref=backref('movie_links'))