from speakerRecognition import task_enroll
from speakerRecognition import task_predict
import PySimpleGUI as sg

if __name__ == "__main__":

    mdl = "model2.out"
    task_enroll("./Jackson ./Nicolas ./Jan ./Arjuan", mdl)
    #task_predict("./*.wav", mdl)

    layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]
    # Create the window
    window = sg.Window("Demo", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()


