import ssl
from urllib2 import urlopen
from bs4 import BeautifulSoup
import nltk
import gensim


class nytnpl:
  
  def __init__(self, url):
    self._url = url
    self.text = ''
    self.words = []

  #takes URL and returns the NYT article body
  def scrape(self, url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urlopen(self._url,context=ctx)
    soup = BeautifulSoup(html, 'html.parser')
    ps = soup.find_all('p', class_='story-body-text story-content')
    article = ''
    for p in ps:
      article += p
      
    self.text = article
    return article
    
    
  def tokenize(self, text, how=NULL,stop_file):
    words = nltk.tokenize(text)
    
    #code to look for stop_file first in working directory and then in a custom path
    #cust_words = file.read()
    stop_words = cust_words | nltk.corpus.stopwords.words('english')
    
    if (how="all"){
      #removes stop words
      words = [word for word in words not in stop_words]
      
      #removes punctuation
      words = [word for word in words if len(word)>1]
      
      #lemmatizes
      words = [nltk.WordNetLemmatizer.lemmatize(word) for word in words]
    }
    
    self.words = words
    return words
    
  def guess_subject(self, words):
  
  
  #generates the word2vec representation based on the object's article and supplied word
  def get_wordVec(self, word):
    w2v_model = gensim.models.word2vec.Word2Vec(self.words, size = 300)
    return w2v_model[word]
  
  #returns the document representation based on the supplied list of gen_docs  
  def get_doc2vec(self, gen_docs):
    gen_docs.append(self.words)
    tagged_documents = []
    for i,sent in enumerate(gen_docs):
      tagged_documents.append(gensim.models.doc2vec.TaggedDocument(gen_doc, ["sent_{}".format(i)]))
      d2v_model = gensim.models.doc2vec.Doc2Vec(tagged_documents,size=300)
      
    return d2v_model.infer_vector(self.words)
      
  
  
   
    
    
