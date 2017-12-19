import requests
from bs4 import BeautifulSoup
import json


API_ROOT = 'http://api.nytimes.com/svc/search/v2/articlesearch.'

API_SIGNUP_PAGE = 'http://developer.nytimes.com/docs/reference/keys'

class NoAPIKeyException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class articleAPI(object):
    def __init__(self, key = None):
        """
        Initializes the articleAPI class with a developer key. Raises an exception if a key is not given.
        
        Request a key at http://developer.nytimes.com/docs/reference/keys
        
        :param key: New York Times Developer Key
        
        """
        self.key = key
        self.response_format = 'json'
        self.response = {}
        self.urls = []
        self.articles = []
        
        if self.key is None:
            raise NoAPIKeyException('Warning: Missing API Key. Please visit ' + API_SIGNUP_PAGE + ' to register for a key.')
    
    def _utf8_encode(self, d):
        """
        Ensures all values are encoded in UTF-8 and converts them to lowercase
        
        """
        for k, v in d.items():
            if isinstance(v, str):
                d[k] = v.encode('utf8').lower()
            if isinstance(v, list):
                for index,item in enumerate(v):
                    item = item.encode('utf8').lower()
                    v[index] = item
            if isinstance(v, dict):
                d[k] = self._utf8_encode(v)
        
        return d
    
    def _bool_encode(self, d):
        """
        Converts bool values to lowercase strings
        
        """
        for k, v in d.items():
            if isinstance(v, bool):
                d[k] = str(v).lower()
        
        return d

    def _options(self, **kwargs):
        """
        Formats search parameters/values for use with API
        
        :param \*\*kwargs: search parameters/values
        
        """
        def _format_fq(d):
            for k,v in d.items():
                if isinstance(v, list):
                    d[k] = ' '.join(map(lambda x: '"' + x + '"', v))
                else:
                    d[k] = '"' + v + '"'
            values = []
            for k,v in d.items():
                value = '%s:(%s)' % (k,v)
                values.append(value)
            values = ' AND '.join(values)
            return values
        
        kwargs = self._utf8_encode(kwargs)
        kwargs = self._bool_encode(kwargs)
        
        values = ''
        
        for k, v in kwargs.items():
            if k is 'fq' and isinstance(v, dict):
                v = _format_fq(v)
            elif isinstance(v, list):
                v = ','.join(v)
            values += '%s=%s&' % (k, v)
        
        return values

    def search(self, 
                response_format = None, 
                key = None, 
                **kwargs):
        """
        Calls the API and returns a dictionary of the search results
        
        :param response_format: the format that the API uses for its response, 
                                includes JSON (.json) and JSONP (.jsonp). 
                                Defaults to '.json'.
                                
        :param key: a developer key. Defaults to key given when the articleAPI class was initialized.
        
        """
        if response_format is None:
            response_format = self.response_format
        if key is None:
            key = self.key
        
        url = '%s%s?%sapi-key=%s' % (
            API_ROOT, response_format, self._options(**kwargs), key
        )
        
        r = requests.get(url)
        self.response = r.json()
        return len(r.json())
    
    def parse_articles(self,articles=None):
            '''
            This function takes in a response to the NYT api and parses
            the articles into a list of dictionaries with URL being the really
            only important key
            '''
            news = []
            articles = self.response
            for i in articles['response']['docs']:
                dic = {}
                dic['url'] = i['web_url']
                # subject
                subjects = []
                for x in range(0,len(i['keywords'])):
                    if 'subject' in i['keywords'][x]['name']:
                        subjects.append(i['keywords'][x]['value'])
                dic['subjects'] = subjects   
                news.append(dic)

    
            for d in news:
                if "url" in d: self.urls.append(d["url"])
            
            articles = []
            for url in self.urls:
                article = ''
                session = requests.Session()
                req=session.get(url)
                soup = BeautifulSoup(req.text,'html.parser')
                paragraphs = soup.find_all('p',class_='story-body-text story-content')
                for p in paragraphs:
                        article = article + p.get_text()
                articles.append(article)
            self.articles = articles
            return(articles)
