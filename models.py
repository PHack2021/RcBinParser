import uuid

from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Integer, MetaData, String, Table, Text, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import ARRAY
from sqlalchemy.dialects.postgresql import UUID

from config import CONNECTION_STRING

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(CONNECTION_STRING)


def create_table(engine):
    Base.metadata.create_all(engine)


class District(Base):
    __tablename__ = 'district'

    code = Column(String(8), primary_key=True, unique=True, nullable=False)
    name = Column(String(5), nullable=False)
    county_city_code = Column(ForeignKey('county_city.code'), nullable=False)
    # county_city_name = Column(ForeignKey('county_city.name'), nullable=False)

    county_city = relationship('County_City', back_populates='districts')
    organizations = relationship('Organization', back_populates='district')


class County_City(Base):
    __tablename__ = 'county_city'

    code = Column(String(5), primary_key=True, unique=True, nullable=False)
    name = Column(String(3), unique=True, nullable=False)
    order = Column(Integer, index=True)
    alt_name = Column(String(3))

    districts = relationship(
        'District', back_populates='county_city', order_by=District.code)


class Organization(Base):
    __tablename__ = 'organization'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, unique=True, nullable=False)
    address = Column(Text)
    contact = Column(Text)
    phone = Column(String(15))
    district_code = Column(ForeignKey('district.code'))

    district = relationship(
        'District', back_populates='organizations', order_by=District.code)
