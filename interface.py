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
                self.gmmset.new_model(feats, name)
                print("Fitted: " + name)
            except Exception as e:
                print("%s failed" % name)

    def dump(self, fname):
        print("Dumping to file")
        with open(fname, 'wb') as f:
            pickle.dump(self, f, -1)

    def verify(self, fs, signal, label):
        try:
            feature = get_feature(fs, signal)
        except Exception as e:
            print(e)
        return self.gmmset.verify_one(feature, label)

    @staticmethod
    def load(fname):
        with open(fname, 'rb') as f:
            return pickle.load(f)
