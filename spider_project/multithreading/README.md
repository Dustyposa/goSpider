## 多线程爬虫

在这里提一个问题：**如果让你在10秒内请求10次，但是每次请求后需要sleep 1秒，这样10次就需要sleep 10s，你该怎么做呢？**

没错，要解决这个问题，多线程爬取就是我们的解决办法之一！  
爬虫最耗费时间的地方是请求与响应的IO，如果每次只发送一个请求，那么他就会一直等待该请求的响应，再继续发送另一个请求。是非常耗时的，为了提高爬取效率，我们使用多线程爬虫。

### python多线程实例
   - [豆瓣top250多线程抓取源码](./douban_top250.py)（源码较简单，如果需要解析的话请提issue，回头填坑）
    ![豆瓣movieTop250](./mul_example/douban250.gif)
#### 1. 让一个函数同时执行多次
导入多线程与时间模块
```python
>>> import threading
>>> import time
```
定义线程运行的函数
```python
def fun(thread_name, others):
    for i in range(3):
        print(f"线程{thread_name}准备休息{others}秒")
        time.sleep(2)
        print(f"this is a treading, my name is {thread_name}")
```
开启两个线程并运行
 - Thread 对象
   - target # 线程执行函数
   - args  # 函数位置参数
   - kwargs  # 函数关键字参数
   - 方法
        - .start()  # 开始运行线程
        - .join()  # 主线程等待子线程函数的运行结束，否则会造成孤儿进程。 
```python
threading_list = []  # 创建线程容器

t1 = threading.Thread(target=fun, args=("thread-1", 2))  # 创建线程对象1
t2 = threading.Thread(target=fun, args=("thread-2", 1))  # 创建线程对象2
threading_list.append(t1)  # 加入线程容器
threading_list.append(t2)
list(map(lambda x: x.start(), threading_list))  # start 用来执行线程
list(map(lambda t: t.join(), threading_list))  # join用于主线程等待子线程运行结束
print("主线程运行结束。")
```
结果如下：
![多线程示例](./mul_example/mul.gif)
我们可以看到函数是同时执行的，代码执行总时长也是远少于 6 + 3 = 9s的，并且两个线程执行顺序也是随机的。
这就达到我们想要的效果啦！  
#### [多线程示例完整代码](./mul_example/mul_treading_exmple.py)
#### 2. 多线程的同步问题
但是，多线程也会有问题，接下来我们用下面的示例来看一下

设定一个全局计数变量`count`  
```python
>>> count = 0
```

设定计数函数 `count_fun`,函数功能也很简单。用来对全局变量`count`进行不断的累加至100万次。
```python
def count_fun():
    global count
    for i in range(1000000):
        count += 1

```
我们运行的主函数，与上一个示例相似，只是没有传递额外的参数。
```python
threading_list = []

t1 = threading.Thread(target=count_fun)
t2 = threading.Thread(target=count_fun)
threading_list.append(t1)
threading_list.append(t2)

list(map(lambda x: x.start(), threading_list))
list(map(lambda t: t.join(), threading_list))
print(f"主线程运行结束。count is : {count}")
```

该次运行结果如下图:
```python
主线程运行结束。count is : 1550720
```
#### [线程同步问题代码](./mul_example/mul_questiion.py)
没错，结果并不是200万，这就是线程的**同步问题**。  
因为变量公用，那么两个线程获取到的变量值可能是同样的，因为赋值操作还没执行。
有一个简单的解决办法，我们可以为操作变量时加上线程锁来解决这个问题。
代码示例如下：
我们初始化一个线程锁对象：
```python
>>> lock = threading.Lock()
```
在对公用变量操作时，我们上锁
```python
def count_fun():
    global count
    for i in range(1000000):
        with lock:  # 在执行对公用变量操作时，加上锁，以此来保证线程的安全性
            count += 1
```
输出结果如下：
```python
主线程运行结束。count is : 2000000
```
#### [线程锁完整代码](./mul_example/mul_lock.py)
有了这两步，我们就能完成多线程爬虫啦！
