from sklearn.mixture import GaussianMixture
import operator
import numpy as np
import math


class GMMSet:

    def __init__(self):
        self.gmm_order = 32
        self.gmms = []
        self.labels = []

    def fit_new(self, x, label):
        self.labels.append(label)
        gmm = GaussianMixture(self.gmm_order)
        gmm.fit(x)
        self.gmms.append(gmm)

    def predict_one(self, x):
        scores = [self.gmm_score(gmm, x) for gmm in self.gmms]
        print(scores)
        # p = sorted(enumerate(scores), key=operator.itemgetter(1), reverse=True)
        # p = [(str(self.y[i]), y, p[0][1] - y) for i, y in p]
        result = [(self.labels[index], value) for (index, value) in enumerate(scores)]
        #[print(self.y[index], value) for (index, value) in enumerate(scores)]
        p = max(result, key=operator.itemgetter(1))
        softmax_score = self.softmax(scores)
        return p[0], softmax_score

    @staticmethod
    def gmm_score(gmm, x):
        e = gmm.score(x)
        return np.sum(e) / len(x)

    @staticmethod
    def softmax(scores):
        scores_sum = sum([math.exp(i) for i in scores])
        score_max = math.exp(max(scores))
        return round(score_max / scores_sum, 3)
