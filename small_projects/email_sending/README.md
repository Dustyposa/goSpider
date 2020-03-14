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
  + `pyinstaller -wF email_gui.py`  # 普通运行 + GUI + 单文件打包
  + `pyinstaller -wF sche_email_sending.py -n 邮件小助手`  # 调度器运行 + GUI + 单文件打包
  + `pyinstaller -w sche_email_sending.py -n 邮件小助手`  # 多文件打包 + GUI
- Authentication error
  + 检查第三方邮箱 smtp 接口是否开启
  + check the third part is enabled your account's `smtp server`
