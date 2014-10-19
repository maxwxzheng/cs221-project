from sqlalchemy import Column, Integer, String

from base import Base


class CompanyType(Base):
    __tablename__ = 'company_type'

    id = Column(Integer, primary_key=True)
    kind = Column(String(32))