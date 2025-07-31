import PySimpleGUI as sg

layout = [
    [sg.Text("Enter something:"), sg.InputText()],
    [sg.Checkbox("Check me!")],
    [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), key='slider')],
    [sg.Button("OK")]
]

window = sg.Window("Demo", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    print(event, values)

window.close()
