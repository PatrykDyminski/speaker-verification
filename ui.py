from speakerRecognition import task_enroll
from speakerRecognition import task_predict_single
from recorder import record
import PySimpleGUI as sg

if __name__ == "__main__":

    mdl = "model2.out"
    task_enroll("./Jackson ./Nicolas ./Jan ./Arjuan ./Patryk", mdl)

    layout = [[sg.Text("Naciśnij przycisk aby rozpocząć weryfikację mówcy")], [sg.Button("Rozpocznij weryfikacje")]]
    window = sg.Window("Super Rozpoznawacz", layout, margins=(200, 200))

    while True:
        event, values = window.read()
        if event == "Rozpocznij weryfikacje":
            recording = record()
            label, score = task_predict_single(recording, mdl)
            sg.popup(label + " " + str(score))

            print(label + " " + str(score))

        if event == sg.WIN_CLOSED:
            break

    window.close()


