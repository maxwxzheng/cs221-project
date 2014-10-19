from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base


"""This table doesn't seem particularly useful.  Looks like it just can be used
to tell if a movies cast and crew is complete or complete and verified"""

class CompleteCast(Base):
    __tablename__ = 'complete_cast'

    id = Column(Integer, primary_key=True)

    movie_id = Column(Integer, ForeignKey('title.id'))
    movie = relationship("Movie", backref=backref('complete_cast'))

    subject_id = Column(Integer, ForeignKey('comp_cast_type.id'))
    subject = relationship("CastType", foreign_keys='CompleteCast.subject_id')

    status_id = Column(Integer, ForeignKey('comp_cast_type.id'))
    status = relationship("CastType", foreign_keys='CompleteCast.status_id')
