import urllib2
from bs4 import BeautifulSoup
import re
from download import download_file
import logging

'''logging.basicConfig(
    filename="/home/steveisredatw/task.log",
    level=logging.DEBUG
)'''

logging.info("[start script]")
page_url = "http://103.251.43.52/lottery/weblotteryresult.php"

page = urllib2.urlopen(page_url)

soup = BeautifulSoup(page,'html.parser')

links = soup.findAll('a', attrs={'href': re.compile("^javascript:")})

for link in links:
    href = link.get('href')
    href_no = re.findall(r'(\d+)', href)
    download_file(str("tmp"+href_no[0]))

logging.info("[end script]")
