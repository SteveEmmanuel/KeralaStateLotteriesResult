from app import db
from datetime import datetime
from magicJSON import MagicJSON

class Lottery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    series = db.Column(db.String(120), unique=True, nullable=False)
    details = db.Column(MagicJSON(nullable=False))

    def __repr__(self):
        return '<Lottery %r>' % self.name

    def __init__(self, date, name, series, details):
        """"""
        self.date = date
        self.name = name
        self.series = series
        self.details = details

