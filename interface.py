import pickle
from collections import defaultdict
from skgmm import GMMSet
from features import get_feature


class ModelInterface:

    def __init__(self):
        self.features = defaultdict(list)
        self.gmmset = GMMSet()

    def enroll(self, name, fs, signal):
        feat = get_feature(fs, signal)
        self.features[name].extend(feat)

    def train(self):
        self.gmmset = GMMSet()
        for name, feats in self.features.items():
            try:
                self.gmmset.fit_new(feats, name)
            except Exception as e:
                print("%s failed" % (name))

    def dump(self, fname):
        """ dump all models to file"""
        with open(fname, 'wb') as f:
            pickle.dump(self, f, -1)

    def predict(self, fs, signal):
        """
        return a label (name)
        """
        try:
            feature = get_feature(fs, signal)
        except Exception as e:
            print(e)
        return self.gmmset.predict_one(feature)

    @staticmethod
    def load(fname):
        """ load from a dumped model file"""
        with open(fname, 'rb') as f:
            return pickle.load(f)
