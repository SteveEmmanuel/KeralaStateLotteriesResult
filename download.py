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
directory = os.path.dirname(os.path.realpath(__file__))+"/pdf/"

def download_file(file_name):
    file_url = base_url+file_name+".pdf"

    # URL of the lottery result to be downloaded is defined as image_url
    r = requests.get(file_url)  # create HTTP response object

    # send a HTTP request to the server and save
    # the HTTP response in a response object called r
    with open(os.path.join(directory, file_name+".pdf"), 'wb') as f:
        # Saving received content as a png file in
        # binary format

        # write the contents of the response (r.content)
        # to a new file in binary mode.
        f.write(r.content)
    scrape_dict = scrape_pdf(directory+file_name+".pdf")
    print(scrape_dict)
    logging.info(scrape_dict)
    date = datetime.strptime(scrape_dict['info']['date'], '%d/%m/%Y')
    series = re.findall(r'([\w-]*)(th|rd|nd|st)', scrape_dict['info']['series']).pop()[0]
    exists = db.session.query(Lottery.id).filter_by(series=series).scalar() is not None
    url = file_url
    with open(os.path.join(directory, file_name+".pdf"), "rb") as pdf_file:
        pdf_base_64 = base64.b64encode(pdf_file.read())
    if not exists:
        lottery = Lottery(name=scrape_dict['info']['name'], series=series,
                          date=date, details=scrape_dict['prizes'],
                          pdf_base_64=pdf_base_64, url=file_url)
        db.session.add(lottery)
        try:
            db.session.commit()
            logging.info("commit success" + lottery.series)
        except Exception as e:
            logging.info("commit failed"+ lottery.series)
    #query = db.session.query(Lottery)
    #q = query.all()