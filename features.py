import numpy as np
from python_speech_features import mfcc
from sklearn import preprocessing
import sys


def get_feature(fs, signal):
    mfcc_feature = mfcc(
        signal,
        samplerate=fs,
        winlen=0.032,
        winstep=0.016,
        preemph=0.95,
        nfft=1024,
        winfunc=np.hamming,
        nfilt=30)
    mfcc_feature = preprocessing.scale(mfcc_feature)
    if len(mfcc_feature) == 0:
        print >> sys.stderr, "ERROR.. failed to extract mfcc feature:", len(signal)
    return mfcc_feature

