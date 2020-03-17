## packaging cmd
```shell script
pyinstaller -w email_gui.py
```
### install pyinstaller
```shell script
python -m pip install pyinstaller
```
#### issue
- unicode_error
  + `chcp 65001`  

- Authentication error
  + 检查第三方邮箱 smtp 接口是否开启
  + check the third part is enabled your account's `smtp server`
  
- `.env` 格式说明(`dotenv`使用)
  + ```ENV_VARIABLE_NAME=value```
- 其余打包方式
   > `pyinstaller -wF email_gui.py`  # 普通运行 + GUI + 单文件打包  
  `pyinstaller -wF sche_email_sending.py -n 邮件小助手`  # 调度器运行 + GUI + 单文件打包  
  `pyinstaller -w sche_email_sending.py -n 邮件小助手`  # 多文件 + GUI + 调度器打包
- 相关模块说明
    + [yagmail](https://github.com/kootenpv/yagmail) —— 邮件发送
    + [PySimpleGUI](https://pysimplegui.readthedocs.io/) —— GUI
    + [sched](https://docs.python.org/zh-cn/3/library/sched.html?highlight=sched) —— 调度模块（标准库）
    + [dotenv](https://github.com/theskumar/python-dotenv) —— 环境变量加载
- 文件格式说明
    + 发件方邮箱文件(xx.csv)  
    ```
    user1,pwd2
  user2,pwd2
  ```
  + 收件方邮箱文件(xx.csv)
  ```
  email_address1
  email_address2
  email_address3
  email_address4
  ```
