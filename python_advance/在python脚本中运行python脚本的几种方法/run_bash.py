import os

bash_cmd = "bash test.sh"


def system_run() -> None:
    """os.system 运行"""
    print("os.system start!")
    os.system(bash_cmd)


if __name__ == '__main__':
    system_run()
