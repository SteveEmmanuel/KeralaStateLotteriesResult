import requests
from app import app, db
from db_creator import Lottery
from datetime import datetime
from scrape_pdf import scrape_pdf
import os


for file in os.listdir("pdf"):
    scrape_dict = scrape_pdf(file)
    #print scrape_dict
    lottery = Lottery(name=scrape_dict['info']['name'], series=scrape_dict['info']['series'],
                      date=scrape_dict['info']['date'], details=scrape_dict['prizes'])
    db.session.add(lottery)
    db.session.commit()