import os
import subprocess
import time

bash_cmd = "zsh test.sh"
test_bash_file = "test.sh"
zsh_file = "/bin/zsh"
bash_cmd_list = ["bash", "test.sh"]
python_cmd_list = ["python3", "check_alive.py"]


def system_run() -> None:
    """os.system 运行"""
    print("os.system start!")
    os.system(bash_cmd)


def os_popen_run() -> None:
    """使用os.popen 运行子进程"""
    print("Start")
    with os.popen(" ".join(python_cmd_list)) as pipe:
        for line in pipe.readlines():
            print(line, end="")

    """
    with os.popen(bash_cmd) as pipe, open("bash_out.txt", "w", encoding="u8") as fp:
        for line in pipe.readlines():
            print(line, end="", file=fp)
    """


def subprocess_run() -> None:
    proc = subprocess.Popen(
        bash_cmd_list,
        stdout=subprocess.PIPE,
    )
    print(proc.returncode)
    print(proc.poll())
    print(proc.returncode)
    proc.stdout.close()
    print("*" * 50)
    print(proc.wait())


def os_exec_run() -> None:
    """替代当前进程的运行"""
    print("python 正在运行")
    time.sleep(5)
    print("python 运行完毕，执行 bash 脚本")
    os.execv(zsh_file, bash_cmd_list)  # == os.execl(zsh_file, *bash_cmd_list)


if __name__ == '__main__':
    system_run()
    os_exec_run()
    os_popen_run()
    subprocess_run()
