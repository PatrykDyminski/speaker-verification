from sklearn.mixture import GaussianMixture
import operator
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

    def verify_one(self, x, label):
        scores = [self.gmm_score(gmm, x) for gmm in self.gmms]
        results = [(self.labels[index], value) for (index, value) in enumerate(scores)]
        print(max(results, key=operator.itemgetter(1)))
        p = max(results, key=operator.itemgetter(1))
        softmax_score = self.softmax(scores)
        return p[0], softmax_score

    @staticmethod
    def gmm_score(gmm, x):
        score = gmm.score(x)
        return score / len(x)

    @staticmethod
    def softmax(scores):
        scores_sum = sum([math.exp(i) for i in scores])
        score_max = math.exp(max(scores))
        return round(score_max / scores_sum, 3)
