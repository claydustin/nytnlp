# nytnlp
Suite of NLP methods applied to a NYT Articles

## nytapi.py
* Uses NYT's provided API to make HTML requests. 
* Using the search and parse_articles functions you can submit queries to the API and receive JSON documents in return

## nytscrape.py
* Provides word2vec and doc2vec representations of NYT returned articles
* Used in conjunction with nytapi to provide NLP analysis of queried news articles
