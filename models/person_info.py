from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base


class PersonInfo(Base):
    __tablename__ = 'person_info'

    id = Column(Integer, primary_key=True)

    person_id = Column(Integer, ForeignKey('name.id'))
    person = relationship("Person", backref=backref('person_info'))

    info_type_id = Column(Integer, ForeignKey('info_type.id'))
    info_type = relationship("InfoType", backref=backref('person_info'))

    info = Column(String)
    note = Column(String)