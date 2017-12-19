import ssl
from urllib2 import urlopen
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import nltk.WordNetLemmatizer as wln

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
    
  def tokenize(text, stop_file):
    words = nltk.tokenize(text)
    
    #code to look for stop_file first in working directory and then in a custom path
    #cust_words = file.read()
    stop_words = cust_words | stopwords.words('english')
    
    #removes stop words
    words = [word for word in words not in stop_words]
    
    #removes punctuation
    words = [word for word in words if len(word)>1]
    
    #lemmatizes
    words = [wln().lemmatize(word) for word in words]
    
    return words
    
  def guess_subject(words):
    
  def get_docRep(sentences):
    
   
    
    
