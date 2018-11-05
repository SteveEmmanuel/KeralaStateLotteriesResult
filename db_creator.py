from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

from magicJSON import MagicJSON

engine = create_engine('sqlite:///lotteries.db', echo=True)
Base = declarative_base()

class Lottery(Base):
    __tablename__ = 'lotteries'
    id = Column(Integer, primary_key = True)
    date = Column(Date)
    name = Column(String)
    series = Column(String)
    details = Column(MagicJSON)

    def __init__(self, date, name, series, details):
        """"""
        self.date = date
        self.name = name
        self.series = series
        self.details = details

# create tables
Base.metadata.create_all(engine)
