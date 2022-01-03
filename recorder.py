import sounddevice as sd
import soundfile as sf


def record():
    fs = 44100
    duration = 1  # seconds

    recording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float64')
    sd.wait()

    sd.play(recording, fs)
    sd.wait()

    filename = 'output.wav'
    sf.write(filename, recording, fs)

    return filename
