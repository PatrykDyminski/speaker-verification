import os
from os.path import splitext
import numpy as np
from pydub import AudioSegment
from utils import read_wav
from interface import ModelInterface
import soundfile as sf
import csv


def process_files():
    m = ModelInterface()
    mainDir = "dev2"

    def enroll(file, speakerDir):
        if file.endswith(".wav"):
            try:
                fs, signal = read_wav(file)
                m.enroll(speakerDir, fs, signal)
                print("enrolled: " + speakerDir + ": " + file)
            except Exception as e:
                print(file + " error %s" % e)

    traverse_file_tree_and_do_action(mainDir, enroll)

    m.train()
    m.dump("mdl3.out")


def test_model(input_model, label, seconds):
    m = ModelInterface.load(input_model)

    mainDir = "dev-clean"

    results = []

    def test(file, dir):
        if file.endswith(".wav"):
            fs, signal = read_wav(file)
            frames = fs * seconds

            # print(np.shape(signal))

            score = m.verify(fs, signal[:frames], label)
            score = round(score, 4)

            results.append(score)
            print(file + " - " + str(score) + "     " +str(frames/fs))

            if abs(score) < 0.062:
                print("Patryk")
                sf.write("rec" + str(score) + ".wav", signal[:frames], fs)

    traverse_file_tree_and_do_action(mainDir, test)

    print(results)
    print(np.shape(results))

    np.savetxt('results.csv', results, delimiter=',')


def convert_files_to_wav():
    mainDir = "dev2"

    def convert(file):
        if file.endswith(".flac"):
            flac2wav(file)

    traverse_file_tree_and_do_action(mainDir, convert)


def verify_sample(input_file, input_model, labelToVerify):
    m = ModelInterface.load(input_model)
    fs, signal = read_wav(input_file)
    return m.verify(fs, signal, labelToVerify)


def traverse_file_tree_and_do_action(mainDir, action):
    for speakerDir in os.listdir(mainDir):
        d = os.path.join(mainDir, speakerDir)
        if os.path.isdir(d):
            for chapterDir in os.listdir(d):
                ch = os.path.join(d, chapterDir)
                if os.path.isdir(ch):
                    for flacFile in os.listdir(ch):
                        file = os.path.join(ch, flacFile)
                        if os.path.isfile(file):
                            action(file, speakerDir)


def flac2wav(flac):
    wav_path = "%s.wav" % splitext(flac)[0]
    song = AudioSegment.from_file(flac, format="flac")
    song.export(wav_path, format="wav")
