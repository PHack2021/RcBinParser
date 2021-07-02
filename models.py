from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Integer, MetaData, String, Table, Text, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import ARRAY

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

    code = Column(Text, primary_key=True, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    county_city_code = Column(ForeignKey('county_city.code'), nullable=False)

    county_city = relationship('County_City', back_populates='districts')


class County_City(Base):
    __tablename__ = 'county_city'

    code = Column(Text, primary_key=True, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    order = Column(Integer, index=True)
    alt_name = Column(Text)

    districts = relationship(
        'District', back_populates='county_city', order_by=District.code)
