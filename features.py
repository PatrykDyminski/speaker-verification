import numpy as np
from python_speech_features import mfcc
from sklearn import preprocessing
import sys


def get_feature(fs, signal):
    mfcc_feature = mfcc(
        signal,
        samplerate=fs,
        winlen=0.024,
        winstep=0.012,
        nfft=1024,
        preemph=0.95,
        winfunc=np.hamming,
        nfilt=26)
    scaled_features = preprocessing.scale(mfcc_feature)
    if len(mfcc_feature) == 0:
        print >> sys.stderr, "ERROR.. failed to extract mfcc feature:", len(signal)

    #print(mfcc_feature)
    #print(scaled_features)
    #print(np.shape(scaled_features))

    return scaled_features

