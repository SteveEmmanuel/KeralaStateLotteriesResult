from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from magicJSON import MagicJSON
from flask_login import UserMixin
from sqlalchemy.orm import scoped_session, sessionmaker

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

class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100))
    password = Column(String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.user_id

# create tables
Base.metadata.create_all(engine)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()
