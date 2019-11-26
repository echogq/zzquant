# coding: utf-8

from . import *

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float, Boolean, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ModelMixin(object):
    def __init__(self, **kwargs):
        for attr in self.__mapper__.columns.keys():
            if attr in kwargs:
                setattr(self, attr, kwargs[attr])

class Account(Base):
    __tablename__ = 'account_config'
    account_id = Column(String, nullable=False, primary_key=True)
    config = Column(Json, nullable=False)

class Holiday(Base):
    __tablename__ = "holidays"
    __table_args__ = (PrimaryKeyConstraint('region', 'holiday'),)
    region = Column(String)
    holiday = Column(Date)


class Location(Base):
    __tablename__ = "location"
    uid = Column(Integer, primary_key = True)
    info = Column(Json)
