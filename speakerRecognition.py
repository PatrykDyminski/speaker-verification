#!/usr/bin/env python3

import os
import sys
import itertools
import glob
from utils import read_wav
from interface import ModelInterface


def task_enroll(input_dirs, output_model):
    m = ModelInterface()
    input_dirs = [os.path.expanduser(k) for k in input_dirs.strip().split()]
    dirs = itertools.chain(*(glob.glob(d) for d in input_dirs))
    dirs = [d for d in dirs if os.path.isdir(d)]

    if len(dirs) == 0:
        print("No valid directory found!")
        sys.exit(1)

    for d in dirs:
        label = os.path.basename(d.rstrip('/'))
        wavs = glob.glob(d + '/*.wav')

        if len(wavs) == 0:
            print("No wav file found in %s" % d)
            continue
        for wav in wavs:
            try:
                fs, signal = read_wav(wav)
                m.enroll(label, fs, signal)
                print("wav %s has been enrolled" % wav)
            except Exception as e:
                print(wav + " error %s" % e)

    m.train()
    m.dump(output_model)


def task_predict(input_files, input_model):
    m = ModelInterface.load(input_model)
    print('Start prediction')
    # print('Loop before')
    for f in glob.glob(os.path.expanduser(input_files)):
        # print("loop start")
        fs, signal = read_wav(f)
        label, score = m.predict(fs, signal)
        print(f, '->', label, ", score->", score)


def task_predict_single(input_file, input_model):
    m = ModelInterface.load(input_model)
    print('Start prediction')

    fs, signal = read_wav(input_file)
    label, score = m.predict(fs, signal)
    return label, score
