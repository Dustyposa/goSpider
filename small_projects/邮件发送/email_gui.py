import PySimpleGUI as sg

sg.theme('BluePurple')

user_input_key = '-User-'
pwd_input_key = '-PWD-'

layout = [
    [sg.Text('请输入用户名和密码:')],
    [sg.Text('用户名:', size=(14, 1)), sg.Input(key=user_input_key)],
    [sg.Text('密码:', size=(14, 1)), sg.Input(key=pwd_input_key, password_char="*")],
    [sg.Text('发送的邮箱文件:', size=(14, 1)), sg.FileBrowse("浏览", size=(8, 1))],
    [sg.ProgressBar(500, orientation='h', size=(80, 20), key='progbar', style='winnative', relief='52%')],
    [sg.Button('确认'), sg.Button('退出', key='Exit')],
]
window = sg.Window('邮件发送', layout)
while True:
    event, values = window.read()
    user, pwd = values[user_input_key], values[pwd_input_key]
    print(event, values)
    if event in (None, 'Exit'):
        break
    window['progbar'].update_bar(200 + 1)
    # if event == 'Show':
    # Update the "output" text element to be the value of "input" element
    # window['-OUTPUT-'].update(values['-IN-'])
    print(user, pwd)

window.close()
