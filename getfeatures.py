from sklearn.feature_extraction.text import TfidfVectorizer
import string, re
import numpy as np


class Featurize(object):

	def __init__(self):
		self.vectors = None
		self.articles = None
		self.vectorizer = TfidfVectorizer(min_df = 3, ngram_range=(1,3), stop_words='english')

	def fit(self, article_labels):
		article_list = [article for article in article_labels if article[0].split()>20]
		articles = list(zip(*article_labels)[0])
		labels = list(zip(*article_labels)[1])
		return self.vectorizer.fit_transform(articles).toarray(), labels

	def transform(self, articles):

		self.vectors = self.vectorizer.transform(articles).toarray()
		return self.vectors, articles




