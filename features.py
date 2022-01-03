from python_speech_features import mfcc
from sklearn import preprocessing
import sys


def get_feature(fs, signal):
    mfcc_feature = mfcc(signal, fs)
    mfcc_feature = preprocessing.scale(mfcc_feature)
    if len(mfcc_feature) == 0:
        print >> sys.stderr, "ERROR.. failed to extract mfcc feature:", len(signal)
    return mfcc_feature
