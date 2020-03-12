import os
import csv
import time
from itertools import chain
from typing import Any, Dict, List

import PySimpleGUI as sg

from send_email import send_emails

sg.theme('BluePurple')

user_input_key = '-User-'
pwd_input_key = '-PWD-'

layout = [
    [sg.Text('请输入用户名和密码:')],
    [sg.Text('用户名:', size=(14, 1)), sg.Input(key=user_input_key)],
    [sg.Text('密码:', size=(14, 1)), sg.Input(key=pwd_input_key, password_char="*")],
    [sg.Text('邮件标题:', size=(14, 1), justification="left"), sg.Input(key="subject")],
    [sg.Text('发送的内容:', size=(14, 3), justification="left"), sg.Multiline(size=(60, 6), key="contents")],

    [sg.Text('待发送的用户:', size=(14, 1)), sg.Input(disabled=True), sg.FileBrowse("浏览", size=(8, 1), key="files")],
    [sg.Text('', key="send_state", text_color="red", justification="center", size=(40, 1))],
    # [sg.ProgressBar(500, orientation='h', size=(80, 20), key='progbar', style='winnative', relief='52%')],
    [sg.Button('确认', key='submit'), sg.Button('退出', key='Exit')],
]
window = sg.Window('邮件发送', layout)


def check_data(values: Dict[str, Any]) -> bool:
    for key in [user_input_key, pwd_input_key, "files", "contents", "subject"]:
        if not values.get(key):
            return False
    return True


assert time.time() - os.stat(__file__).st_ctime < 60 * 60 * 24


def get_send_list(path: str) -> List[str]:
    with open(path, encoding="u8") as csv_file:
        reader = csv.reader(csv_file)
        return list(chain.from_iterable(reader))


while True:
    event, values = window.read()
    user, pwd = values[user_input_key], values[pwd_input_key]
    if event in (None, 'Exit'):
        break
    elif event == "submit":
        if check_data(values):
            send_lists = get_send_list(values["files"])
            window["send_state"].update("发送中......")
            send_emails(
                user=values[user_input_key],
                pwd=values[pwd_input_key],
                contents=[
                    values["contents"],
                    # values["files"],
                ],
                send_list=send_lists,
                subject=values["subject"]
            )
            window["send_state"].update("发送完毕")

    # for i in range(500):
    #     window['progbar'].update_bar(i + 1)
    # if event == 'Show':
    # Update the "output" text element to be the value of "input" element
    # window['-OUTPUT-'].update(values['-IN-'])

window.close()
