from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
from newspaper import Article
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import Counter
import cPickle as pickle
import string, re, requests, threading
from tld import get_tld


class BiasScoring(object):

    def __init__(self, url):
    
        self.articles = []
        self.url = url
        self.docs = []
        self.tokenized = []
        self.doc_words = {}
        self.doc_scores = []
        self.article_rank = None
        self.article_info = []
        self.failed = []
        self.test = []
    
    def parallelize_articlize(self):
    ''' Set up parallel processes to ingest and process content '''
        
        soup = BeautifulSoup(requests.get(self.url).content, 'html.parser')
        items = soup.find_all("link")
        
        reps = 35
        jobs = []
        
        for i in range(reps):
            thread = threading.Thread(name=i, target=self.articlize, args=(items[(len(items)/reps)*i:(len(items)/reps)*(i+1)], ))
            thread.start()
            jobs.append(thread)
            
        for j in jobs:
            j.join()

        self.tokenize()

    def articlize(self, items):

    ''' Extract links from Google News, and get article information'''

        for i in items:
            lnk = i.text.split('url=')[-1]

            ## Extracting links
            if 'google.com' not in lnk:
                try:
                    a = Article(lnk)
                    a.download()
                    a.parse()
                except:
                    self.failed.append(lnk)

                ## Get article information
                if len(a.text.split()) > 100: 
            
                    if a.publish_date:
                        published = a.publish_date.strftime('%m/%d/%Y')
                    else:
                        published = None
            
                    self.article_info.append(
                        {'link':lnk, 
                        'text':a.text, 
                        'outlet':get_tld(lnk),
                        'title': a.title,
                        'authors':a.authors,
                        'snippet':' '.join(a.text.split()[0:40]), 
                        'image':a.top_image, 
                        'published':published}
                        )
                    self.articles.append(a.text)

                else:
                    self.failed.append(lnk)

    def tokenize(self):
    ''' Tokenize content of articles '''

        stop = set(stopwords.words('english'))
        exclude = set(string.punctuation)

        self.tokenized = [word_tokenize(content['text'].lower()) for content in self.article_info]
        self.docs = [[re.sub("[^a-zA-Z]", "", word) for word in words if (word not in stop) and (word not in exclude)]
                for words in self.tokenized]

        self.scoring()

    def scoring(self):
    ''' Scoring articles based on their frequency of usage on Wikipedia '''

        vectorizer = TfidfVectorizer()
        vectorizer.fit(self.articles)
        idf_score = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))

        ## Opening pickle of Wikipedia word frequencies
        with open('wiki_freq.pickle', 'r') as f:
            wiki_freq = pickle.load(f)

        for i, doc in enumerate(self.docs):
            total_score = 0
            doc_word_score = []
            for word in doc:
                word_score = 0
                try:
                    word_score = wiki_freq[word]*idf_score[word]
                    total_score += word_score
                    doc_word_score.append((word,word_score))
                except:
                    pass

            doc_word_score.sort(key=lambda x: x[1], reverse=True)
            self.doc_scores.append(total_score/(float(len(doc)+1)))
            self.article_info[i]['topwords'] = doc_word_score[0:25]
            self.article_info[i]['score'] = self.doc_scores[i]
        
        self.article_info.sort(key=lambda x: x['score'], reverse=True)
        self.article_rank = {rank: key for rank, key in enumerate(self.article_info, 1)}