from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


"""This table can be used to join people to movies"""

class CastInfo(Base):
    __tablename__ = 'cast_info'

    id = Column(Integer, primary_key=True)

    person_id = Column(Integer, ForeignKey('name.id'))
    person = relationship("Person", backref=backref('cast_info'))

    movie_id = Column(Integer, ForeignKey('title.id'))
    movie = relationship("Movie", backref=backref('cast_info'))

    # I'm not sure what this is, it doesn't map to Role
    person_role_id = Column(Integer)

    note = Column(String)
    nr_order = Column(Integer)

    role_id = Column(Integer, ForeignKey('role_type.id'))
    role = relationship("Role", foreign_keys='CastInfo.role_id', backref=backref('cast_info'))