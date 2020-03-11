import PySimpleGUI as sg

sg.theme('Light Blue 2')

layout = [[sg.Text('Enter 2 files to comare')],
          [sg.Text('File 1', size=(8, 1)), sg.Input(), sg.FileBrowse()],
          [sg.Text('File 2', size=(8, 1)), sg.Input(), sg.FileBrowse()],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('File Compare', layout)

event, values = window.read()
window.close()
print(f'You clicked {event}')
print(f'You chose filenames {values[0]} and {values[1]}')
