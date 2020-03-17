import os
import csv
import sched
import sys
import time
from dataclasses import dataclass
from itertools import chain, repeat
from pathlib import Path
from typing import Any, Dict, List, Sequence, Iterator, Iterable

import PySimpleGUI as sg

from send_email import send_emails

if time.time() - os.stat(sys.argv[0]).st_mtime > 2 * 60 * 60 * 24:
    sys.exit(1)


@dataclass
class UserClass:
    user: str
    pwd: str


def get_send_list(path: str) -> List[str]:
    with open(path, encoding="u8") as csv_file:
        reader = csv.reader(csv_file)
        return list(chain.from_iterable(reader))


def get_user_list(path: str) -> List[UserClass]:
    with open(path, encoding="u8") as csv_file:
        reader = csv.reader(csv_file)
        return list(map(lambda x: UserClass(user=x[0], pwd=x[1]), reader))


def split_sequence(a: Sequence[Any], n: int):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def pack_send_email_and_user(email_path: str, user_path: str) -> Iterator:
    user_lists = get_user_list(user_path)
    email_lists = get_send_list(email_path)
    split_size = len(email_lists) // len(user_lists)
    email_split_data = split_sequence(email_lists, split_size)
    return zip(repeat(user_lists, split_size), email_split_data)


def is_schedule(ty) -> bool:
    return isinstance(ty, sched.scheduler)


if __name__ == '__main__':
    sg.theme('BluePurple')

    layout = [
        [sg.Text('发件箱邮箱文件:', size=(14, 1)), sg.Input(), sg.FileBrowse("浏览", size=(8, 1), key="user_file")],
        [sg.Text('邮件标题:', size=(14, 1), justification="left"), sg.Input(key="subject")],
        [sg.Text('发送的内容:', size=(14, 3), justification="left"), sg.Multiline(size=(60, 6), key="contents")],
        [sg.Text('待发送的用户:', size=(14, 1)), sg.Input(disabled=True), sg.FileBrowse("浏览", size=(8, 1), key="files")],
        [sg.Text('待发送的附件:', size=(14, 1)), sg.Input(disabled=True),
         sg.FilesBrowse("浏览", size=(8, 1), key="attachment")],
        [sg.Text('延迟时间（分钟）：', text_color="blue", justification="center", size=(14, 1)), sg.In(key="delay")],
        # [sg.ProgressBar(500, orientation='h', size=(80, 20), key='progbar', style='winnative', relief='52%')],
        [sg.Button('确认', key='submit'), sg.Button('退出', key='Exit')],
        [sg.Text('没有任务正在进行', key="send_state", text_color="red", justification="left", size=(80, 1))],

    ]
    window = sg.Window('邮件发送', layout)

    Path("sended.txt").write_text("")


    def check_data(values: Dict[str, Any]) -> bool:
        for key in ["files", "contents", "subject", "user_file", "delay"]:
            if not values.get(key):
                return False
        return True


    sch = task_length = None

    while True:
        event, values = window.read(1)

        if event in (None, 'Exit'):
            if is_schedule(sch):
                window["send_state"].update("任务停止中")
                [sch.cancel(e) for e in sch.queue]
            break
        elif event == "submit":
            if check_data(values):
                def create_email_task_by_time(seconds: int, iter_: Iterable):
                    scheduler = sched.scheduler(time.time)
                    content = [values["contents"]]
                    subj = values["subject"]
                    content.extend(values["attachment"].split(";"))
                    for index, user_and_email in enumerate(iter_, 0):
                        users_m, emails = user_and_email
                        for prio, tmp_data in enumerate(zip(users_m, emails), 1):
                            user_m, email = tmp_data
                            scheduler.enter(index * seconds, priority=prio, action=send_emails, kwargs={
                                "user": user_m.user,
                                "pwd": user_m.pwd,
                                "contents": content,
                                "send_list": email,
                                "subject": subj
                            })
                    return scheduler


                window["send_state"].update("任务创建中")
                sch = create_email_task_by_time(
                    int(values["delay"]) * 60,
                    pack_send_email_and_user(
                        user_path=values["user_file"],
                        email_path=values["files"],
                    )
                )
                task_length = len(sch.queue)
            else:
                window["send_state"].update("请补充数据")
        if is_schedule(sch):
            latest_sec = sch.run(False)
            complete_task = task_length - len(sch.queue)
            if latest_sec:
                window["send_state"].update(
                    f"第 {complete_task}/{task_length} 任务进行中, 新任务将在{latest_sec // 60}分{latest_sec % 60:.1f}s后进行")
            if sch.empty():
                window["send_state"].update("所有任务已经完成")
                sch = complete_task = None
    window.close()
