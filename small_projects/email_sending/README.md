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
  + `pyinstaller -w email_gui.py`
- Authentication error
  + 检查第三方邮箱 smtp 接口是否开启
  + check the third part is enabled your count's `smtp server`
