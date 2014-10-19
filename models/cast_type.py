from sqlalchemy import Column, Integer, String

from base import Base


CAST = 'cast'
CAST_ID = 1

CREW = 'crew'
CREW_ID = 2

COMPLETE = 'complete'
COMPLETE_ID = 3

COMPLETE_AND_VERIFIED = 'complete+verified'
COMPLETE_AND_VERIFIED_ID = 4


class CastType(Base):
    __tablename__ = 'comp_cast_type'

    id = Column(Integer, primary_key=True)
    kind = Column(String(32))