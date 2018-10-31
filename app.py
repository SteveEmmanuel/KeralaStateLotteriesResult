from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lotteries.db'
app.secret_key = "thisisthepasswordforkeralastate"

db = SQLAlchemy(app)

import sys
path = '/home/steveisredatw/keralastatelotteriesresult/'
if path not in sys.path:
   sys.path.insert(0, path)

from app import app as application
