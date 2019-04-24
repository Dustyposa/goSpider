import threading

count = 0


def count_fun():
    global count
    for _ in range(1000000):
        count += 1


threading_list = []

t1 = threading.Thread(target=count_fun)
t2 = threading.Thread(target=count_fun)
threading_list.append(t1)
threading_list.append(t2)

list(map(lambda x: x.start(), threading_list))
list(map(lambda t: t.join(), threading_list))
print(f"主线程运行结束。count is : {count}")

