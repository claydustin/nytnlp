import ssl
from urllib2 import urlopen
from bs4 import BeautifulSoup

  #takes URL and returns the NYT article body
  def scrape(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urlopen(url,context=ctx)
    soup = BeautifulSoup(html, 'html.parser')
    ps = soup.find_all('p', class_='story-body-text story-content')
    article = ''
    for p in ps:
      article += p
    return article
    
      
    
