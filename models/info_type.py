from sqlalchemy import Column, Integer, String

from base import Base


RELEASE_DATES_ID = 16
VOTES = 'votes'
VOTES_ID = 100
RATING = 'rating'
RATING_ID = 101
GROSS_ID = 107
GENRE_TYPE_ID = 3
BUDGET_TYPE_ID = 105


class InfoType(Base):
    __tablename__ = 'info_type'

    id = Column(Integer, primary_key=True)
    info = Column(String(32))
