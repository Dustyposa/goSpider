from typing import Any, Dict

import PySimpleGUI as sg

from send_email import send_emails

sg.theme('BluePurple')

user_input_key = '-User-'
pwd_input_key = '-PWD-'

layout = [
    [sg.Text('请输入用户名和密码:')],
    [sg.Text('用户名:', size=(14, 1)), sg.Input(key=user_input_key)],
    [sg.Text('密码:', size=(14, 1)), sg.Input(key=pwd_input_key, password_char="*")],
    [sg.Text('发送的内容:', size=(14, 3), justification="center"), sg.Input(size=(14, 3), key="contents")],

    [sg.Text('发送的邮箱文件:', size=(14, 1)), sg.FileBrowse("浏览", size=(8, 1), key="files")],
    [sg.ProgressBar(500, orientation='h', size=(80, 20), key='progbar', style='winnative', relief='52%')],
    [sg.Button('确认', key='submit'), sg.Button('退出', key='Exit')],
]
window = sg.Window('邮件发送', layout)


def check_data(values: Dict[str, Any]) -> bool:
    for key in [user_input_key, pwd_input_key, "files", "contents"]:
        if not values.get(key):
            return False
    return True


while True:
    event, values = window.read()
    user, pwd = values[user_input_key], values[pwd_input_key]
    print(event, values)
    if event in (None, 'Exit'):
        break
    elif event == "submit":
        if check_data(values):
            send_emails(
                user=values[user_input_key],
                pwd=values[pwd_input_key],
                contents=[
                    values["contents"],
                    values["files"],
                ]
            )
    # for i in range(500):
    #     window['progbar'].update_bar(i + 1)
    # if event == 'Show':
    # Update the "output" text element to be the value of "input" element
    # window['-OUTPUT-'].update(values['-IN-'])
    print(user, pwd)

window.close()
