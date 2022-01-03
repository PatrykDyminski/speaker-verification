import sounddevice as sd
import soundfile as sf
from utils import read_wav


def record():
    fs = 44100
    duration = 1  # seconds

    recording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float64')
    sd.wait()

    filename = 'output.wav'
    sf.write(filename, recording, fs)

    return filename


def play(fname):
    fs, signal = read_wav(fname)
    sd.play(signal, fs)
    sd.wait()
