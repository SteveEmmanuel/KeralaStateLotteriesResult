from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lotteries.db'
app.secret_key = "thisisthepasswordforkeralastate"

db = SQLAlchemy(app)

login_manager = LoginManager(app)

bcrypt = Bcrypt(app)