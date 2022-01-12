from speakerRecognition import process_files
from speakerRecognition import verify_sample
from recorder import record
import PySimpleGUI as sg

if __name__ == "__main__":

    mdl = "mdl3.out"

    #process_files()

    layout = [[sg.Text("Naciśnij przycisk aby rozpocząć weryfikację mówcy")], [sg.Button("Rozpocznij weryfikacje")]]
    window = sg.Window("Super Rozpoznawacz", layout, margins=(200, 200))

    while True:
        event, values = window.read()
        if event == "Rozpocznij weryfikacje":
            recording = record()
            label, score = verify_sample(recording, mdl, "Patryk")
            sg.popup(label + " " + str(score))

            #play(recording)
            print(label + " " + str(score))

        if event == sg.WIN_CLOSED:
            break

    window.close()


