from sqlalchemy import Column, Integer, String

from base import Base


class LinkType(Base):
    __tablename__ = 'link_type'

    id = Column(Integer, primary_key=True)
    link = Column(String(32))