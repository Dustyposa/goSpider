from typing import List

import yagmail


def send_emails(
        user: str,
        pwd: str,
        contents: List[str],
        send_list: List[str]
) -> None:
    yag = yagmail.SMTP(user=user, password=pwd, host='smtp.163.com')
    yag.send(send_list, contents)


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()
    # 链接邮箱服务器
    yag = yagmail.SMTP(user=os.getenv("USER_NAME"), password=os.getenv("USER_PWD"), host='smtp.163.com')

    # 邮箱正文
    contents = [
        '这是一封正常邮件，需要测试',
        'You can find an audio file attached.',
        # yagmail.inline("./Snipaste_2020-03-09_23-25-23.png"),
        "./Snipaste_2020-03-09_23-25-23.png",
    ]

    # 发送邮件
    yag.send(os.getenv("SEND_EMAIL"), '重要消息cc', contents)
    print("发送成功")
