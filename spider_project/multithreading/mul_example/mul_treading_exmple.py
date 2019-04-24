import threading
import time


def fun(thread_name, others):
    for _ in range(3):
        print(f"线程{thread_name}准备休息{others}秒")
        time.sleep(2)
        print(f"this is a treading, my name is {thread_name}")


threading_list = []

t1 = threading.Thread(target=fun, args=("thread-1", 2))
t2 = threading.Thread(target=fun, args=("thread-2", 1))
threading_list.append(t1)
threading_list.append(t2)
input()
list(map(lambda x: x.start(), threading_list))
list(map(lambda t: t.join(), threading_list))
print("主线程运行结束。")
