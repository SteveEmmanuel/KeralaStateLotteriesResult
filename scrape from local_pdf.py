import requests
from app import db
from app import Lottery
from scrape_pdf import scrape_pdf
import re
import os
from datetime import datetime
import logging
import base64


'''logging.basicConfig(
    filename="/home/steveisredatw/task.log",
    level=logging.DEBUG
)'''
base_url = "http://103.251.43.52/lottery/reports/draw/"

def download_file(file_name):
    scrape_dict = scrape_pdf('pdf/'+file_name)
    print(scrape_dict)
    logging.info(scrape_dict)
    date = datetime.strptime(scrape_dict['info']['date'], '%d/%m/%Y')
    series = re.findall(r'([\w-]*)(th|rd|nd|st)', scrape_dict['info']['series']).pop()[0]

    db.session.rollback()

    query = db.session.query(Lottery).filter_by(series=series)
    exists = bool(query.count())
    url = base_url+filename
    with open('pdf/'+file_name, "rb") as pdf_file:
        pdf_base_64 = base64.b64encode(pdf_file.read())
    if not exists:
        lottery = Lottery(name=scrape_dict['info']['name'], series=series,
                          date=date, details=scrape_dict['prizes'],
                          pdf_base_64=pdf_base_64, url=url)
        db.session.add(lottery)
    else:
        lottery = query.first()
        lottery.name = scrape_dict['info']['name']
        lottery.series = series
        lottery.date = date
        lottery.details = scrape_dict['prizes']
        lottery.pdf_base_64 = pdf_base_64
        lottery.url = url
    try:
        db.session.commit()
        logging.info("commit success" + lottery.series)
    except Exception as e:
        logging.info("commit failed" + lottery.series)
        db.session.rollback()

for root, dirs, files in os.walk("pdf"):
    for filename in files:
        download_file(filename)