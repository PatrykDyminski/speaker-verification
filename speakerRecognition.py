#!/usr/bin/env python3

import os
import sys
import itertools
import glob
from os.path import splitext

from pydub import AudioSegment

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


def task_enroll2():

    m = ModelInterface()

    mainDir = "dev-clean"

    for speakerDir in os.listdir(mainDir):
        d = os.path.join(mainDir, speakerDir)
        if os.path.isdir(d):
            for chapterDir in os.listdir(d):
                ch = os.path.join(d, chapterDir)
                if os.path.isdir(ch):
                    for flacFile in os.listdir(ch):
                        file = os.path.join(ch, flacFile)
                        if os.path.isfile(file):
                            if file.endswith(".wav"):
                                try:
                                    fs, signal = read_wav(file)
                                    m.enroll(speakerDir, fs, signal)
                                    print("enrolled: " + speakerDir + ": " + file)
                                except Exception as e:
                                    print(file + " error %s" % e)

    m.train()
    m.dump("mdl3.out")


def convert_files_to_wav():
    mainDir = "dev-clean"

    for speakerDir in os.listdir(mainDir):
        d = os.path.join(mainDir, speakerDir)
        if os.path.isdir(d):
            print(d)
            for chapterDir in os.listdir(d):
                ch = os.path.join(d, chapterDir)
                if os.path.isdir(ch):
                    print("-" + ch)
                    for flacFile in os.listdir(ch):
                        file = os.path.join(ch, flacFile)
                        if os.path.isfile(file):
                            if file.endswith(".flac"):
                                print("--" + file)
                                flac2wav(file)


def flac2wav(flac):
    wav_path = "%s.wav" % splitext(flac)[0]
    song = AudioSegment.from_file(flac, format="flac")
    song.export(wav_path, format="wav")


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
    fs, signal = read_wav(input_file)
    label, score = m.predict(fs, signal)
    return label, score
