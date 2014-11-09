from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base


class MovieCompanies(Base):
    __tablename__ = 'movie_companies'

    id = Column(Integer, primary_key=True)

    movie_id = Column(Integer, ForeignKey('title.id'))
    movie = relationship("Movie", backref=backref('movie_companies'))

    company_id = Column(Integer, ForeignKey('company_name.id'))
    company = relationship("Company", backref=backref('movie_companies'))

    company_type_id = Column(Integer, ForeignKey('company_type.id'))
    company_type = relationship("CompanyType", backref=backref('movie_companies'))

    note = Column(String)
