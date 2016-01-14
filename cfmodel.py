import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class MyModel():

    def __init__(self):
        self.model = Pipeline([('scale', StandardScaler()), ('model', svm.SVC(kernel='linear', probability=True))])

    def fit(self,X,y,sample_weight=None):
        self.model.fit(X, y)

    def predict(self, X):
        pred = self.model.predict(X)
        pred_prob = self.model.predict_proba(X)

        ''' change threshold for conservative articles. if the probability of the article being 
        conservative is less than 50%, then make the article neutral'''

        for num in xrange(len(X)):
            if (pred_prob[num][np.argmax(pred_prob[num])] < 0.5) and (pred[num]==-1):
                pred[num] = 0
        return pred