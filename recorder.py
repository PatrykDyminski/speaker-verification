import sounddevice as sd
import soundfile as sf


def record():
    fs = 44100
    duration = 1  # seconds
    recording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float64')
    print("Recording Audio")
    sd.wait()
    print("Audio recording complete , Play Audio")
    sd.play(recording, fs)
    sd.wait()
    print("Play Audio Complete")

    filename = 'output.wav'

    sf.write(filename, recording, fs)

    return filename
