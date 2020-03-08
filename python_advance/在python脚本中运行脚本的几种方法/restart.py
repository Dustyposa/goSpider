import os
import sys
import time

def run(select_data: str) -> None:
    if select_data == "a":
        print("程序休眠1s")
        time.sleep(1)
    elif select_data == "b":
        print("程序即将重启")
        os.execv(sys.executable, ["python3"] + sys.argv)  # 或者 ["python3", __file__]
    elif select_data == "c":
        print("程序即将退出")
        sys.exit(0)


if __name__ == '__main__':
    print("程序启动了！")
    print("请选择功能：", "A. sleep 1 s", "B. 重启程序", "C. 结束程序", sep="\n")
    while True:
        select = input("请选择：").lower()
        run(select)
