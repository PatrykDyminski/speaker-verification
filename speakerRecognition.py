import os
from os.path import splitext
from pydub import AudioSegment
from utils import read_wav
from interface import ModelInterface


def process_files():
    m = ModelInterface()

    def enroll(file, speakerDir):
        if file.endswith(".wav"):
            try:
                fs, signal = read_wav(file)
                m.enroll(speakerDir, fs, signal)
                print("enrolled: " + speakerDir + ": " + file)
            except Exception as e:
                print(file + " error %s" % e)

    traverse_file_tree_and_do_action(enroll)

    m.train()
    m.dump("mdl3.out")


def convert_files_to_wav():

    def convert(file):
        if file.endswith(".flac"):
            flac2wav(file)

    traverse_file_tree_and_do_action(convert)


def verify_sample(input_file, input_model, labelToVerify):
    m = ModelInterface.load(input_model)
    fs, signal = read_wav(input_file)
    return m.verify(fs, signal, labelToVerify)


def traverse_file_tree_and_do_action(action):
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
                            action(file, speakerDir)


def flac2wav(flac):
    wav_path = "%s.wav" % splitext(flac)[0]
    song = AudioSegment.from_file(flac, format="flac")
    song.export(wav_path, format="wav")
