from sqlalchemy import Column, Integer, String

from base import Base


class Company(Base):
    __tablename__ = 'company_name'

    id = Column(Integer, primary_key=True)

    name = Column(String(65535))

    country_code = Column(String(255))

    imdb_id = Column(Integer)

    name_pcode_nf = Column(String(5))
    name_pcode_sf = Column(String(5))

    md5sum = Column(String(32))