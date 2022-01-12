from sklearn.mixture import GaussianMixture


class GMMSet:

    def __init__(self):
        self.gmm_order = 32
        self.gmms = []
        self.labels = []

    def new_model(self, x, label):
        self.labels.append(label)
        gmm = GaussianMixture(self.gmm_order)
        gmm.fit(x)
        self.gmms.append(gmm)

    def verify_one(self, x, label):
        idx = self.labels.index(label)
        gmm = self.gmms[idx]

        score = self.gmm_score(gmm, x)
        return score

    @staticmethod
    def gmm_score(gmm, x):
        score = gmm.score(x)
        return score / len(x)
