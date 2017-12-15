import ssl
from urllib2 import urlopen
from bs4 import BeautifulSoup


  def scrape(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urlopen(url,context=ctx)
    soup = BeautifulSoup(html)
    
