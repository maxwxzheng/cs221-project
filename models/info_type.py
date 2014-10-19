from sqlalchemy import Column, Integer, String

from base import Base


RELEASE_DATES_ID = 16
VOTES = 'votes'
VOTES_ID = 100
RATING = 'rating'
RATING_ID = 101
GROSS_ID = 107


class InfoType(Base):
    __tablename__ = 'info_type'

    id = Column(Integer, primary_key=True)
    info = Column(String(32))