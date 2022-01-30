from speakerRecognition import process_files
from speakerRecognition import verify_sample
from speakerRecognition import test_model
from recorder import record
import PySimpleGUI as sg

if __name__ == "__main__":

    mdl = "mdl3.out"
    label = "patryk"
    test_dir = "dev-clean"
    seconds = 3
    threshold = 0.062

    # process_files()
    test_model(mdl, label, seconds, test_dir)

    layout = [[sg.Text("Naciśnij przycisk aby rozpocząć weryfikację mówcy")], [sg.Button("Rozpocznij weryfikacje")]]
    window = sg.Window("Super Rozpoznawacz", layout, margins=(200, 200))

    while True:
        event, values = window.read()
        if event == "Rozpocznij weryfikacje":

            recording = record(seconds)
            score = verify_sample(recording, mdl, label)

            if abs(score) < threshold:
                text = "Witaj Patryk"
            else:
                text = "To nie Patryk"

            sg.popup(text + " " + str(score))

        if event == sg.WIN_CLOSED:
            break

    window.close()
