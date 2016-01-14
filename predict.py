import cPickle as pickle
import cfmodel
from getfeatures import Featurize

class Predict(object):

	def __init__(self):
		self.articles_zipped = None

	def featurize_predict(self, articles):

	    with open('featurize.pickle', 'r') as f:
	        featurize = pickle.load(f)

		X, self.articles = featurize.transform(articles)

		return self.predict(X)

	def predict(self, X):

		with open('model.pickle', 'r') as f:
			model = pickle.load(f)

		pred = model.predict(X)

		return pred, self.articles
