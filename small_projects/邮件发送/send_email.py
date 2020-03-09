import os

import yagmail
from dotenv import load_dotenv

load_dotenv()
# 链接邮箱服务器
yag = yagmail.SMTP(user=os.getenv("USER_NAME"), password=os.getenv("USER_PWD"), host='smtp.163.com')

# 邮箱正文
contents = ['This is the body, and here is just text http://somedomain/image.png',
            'You can find an audio file attached.']

# 发送邮件
yag.send(os.getenv("SEND_EMAIL"), 'subject', contents)

