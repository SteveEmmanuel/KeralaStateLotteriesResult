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

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lotteries.db'
app.secret_key = "thisisthepasswordforkeralastate"

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

# create tables
Base.metadata.create_all(engine)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()
