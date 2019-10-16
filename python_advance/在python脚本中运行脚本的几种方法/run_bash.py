import os
import sys
import time

bash_cmd = "zsh test.sh"
test_bash_file = "test.sh"
zsh_file = "/bin/zsh"
bash_cmd_list = ["bash", "test.sh"]


def system_run() -> None:
    """os.system 运行"""
    print("os.system start!")
    os.system(bash_cmd)


def os_popen_run() -> None:
    os.popen()
    os.execl()


def os_exec_run() -> None:
    """替代当前进程的运行"""
    print("python 正在运行")
    time.sleep(5)
    print("python 运行完毕，执行 bash 脚本")
    os.execv(zsh_file, bash_cmd_list)  # == os.execl(zsh_file, *bash_cmd_list)


if __name__ == '__main__':
    # system_run()
    os_exec_run()
