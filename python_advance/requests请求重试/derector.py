import time


def count_fun_time(func):
    def wrapper(*arg, **kwargs):
        start_time = time.time()
        res = func(*arg, **kwargs)
        print(f"函数总共运行了{time.time() - start_time:.2f}s")
        return res

    return wrapper


def my_function(time_wait: int = 3):
    time.sleep(time_wait)
    print("运行结束")


@count_fun_time
def your_function(time_wait: int = 3):
    time.sleep(time_wait)
    print("运行结束")


my_function = count_fun_time(my_function)
my_function()
my_function(4)

your_function()
your_function(4)
