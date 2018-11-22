from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from magicJSON import MagicJSON
from flask_login import UserMixin
from sqlalchemy.orm import scoped_session, sessionmaker


RC_SITE_KEY = '6LdKYnwUAAAAANaFrlhE78bfFmJl2F-ZEPYeaVyh'
RC_SECRET_KEY = '6LdKYnwUAAAAACt5cz4Qne0eYkJvYNYlmBm97fzI'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///lotteries.db'
SECRET_KEY = 'kLRJ7gT64FWASZmwOOJPrFAlUrWFzHCi'

class Config(object):
    SECRET_KEY = SECRET_KEY
    RECAPTCHA_PUBLIC_KEY = RC_SITE_KEY
    RECAPTCHA_PRIVATE_KEY = RC_SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = SQLALCHEMY_TRACK_MODIFICATIONS
    SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)

bcrypt = Bcrypt(app)

engine = create_engine('sqlite:///lotteries.db', echo=True)
Base = declarative_base()

class Lottery(db.Model):
    __tablename__ = 'lotteries'
    id = Column(Integer, primary_key = True)
    date = Column(Date)
    name = Column(String)
    series = Column(String)
    details = Column(MagicJSON)
    pdf_base_64 = Column(String)
    url = Column(String)

    def __init__(self, date, name, series, details, pdf_base_64, url):
        """"""
        self.date = date
        self.name = name
        self.series = series
        self.details = details
        self.pdf_base_64 = pdf_base_64
        self.url = url

class User(UserMixin, db.Model):
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

class FeedBack(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    comment = Column(String)

# create tables
Base.metadata.create_all(engine)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()
