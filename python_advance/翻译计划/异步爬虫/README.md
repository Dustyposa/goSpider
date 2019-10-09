## 异步网络爬虫
> 作者：  
> A. Jesse Jiryu Davis  
> Guido van Rossum  
>
> 原文链接：[http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html)
>
> 翻译:  
> Dustyposa

### 背景介绍
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 经典的计算机科学更着力于让计算机高效地完成计算的算法。但是许多与网络有关的程序并不是因为计算而耗费大量时间。而是因为程序需要维持大量传输很慢或者闲置的连接。这些程序都面临着不一样的挑战：需要高效地等待大量的网络连接。现在的一种解决方案是非同步I/O,也叫做"异步"。  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本章介绍一个简单的web爬虫。爬虫是一个典型的异步应用，因为它需要等待很多响应，而很少做计算任务。只要能够抓取到更多的页面，程序就能运行的更快。如果为每一个进行中的请求分配一个线程，那么随着大量并发请求的增加，在耗尽所有socket对象之前，内存或者线程相关的资源[^1]就会先被耗尽了。  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们会分三个阶段展示代码。第一阶段，我们展示一个异步事件循环并***编写or描述***一个使用带有回调的事件循环的爬虫：这非常高效，但是当代码拓展到解决更复杂的问题时将会导致代码极难维护，变成面条式代码（`spaghetti code`）。第二阶段，因此，我们会展示兼顾高效和可拓展性强的`Python`协程。我们会在`python`中使用生成器实现几个协程的例子。在第三阶段，我们使用来自`python`标准库中功能更全面的`asyncio`协程库，并使用异步队列协调任务。

### 任务
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;编写一个发现和下载目标网站上所有页面的爬虫，用来存档或者做索引。从一个根URL开始，抓取每个页面，然后解析页面并获取未显示页面的链接，并且将解析url加入一个队列。当抓到一个没有任何链接并且待抓取队列为空时停止抓取。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们可以通过同时抓取多个页面来加速这个过程。当爬虫发现新的链接时，在不同的套接字上对新页面进行同步抓取。当响应返回时进行解析，将新链接加入队列。由于过多的并发会降低抓取性能，所以抓取的速度会越来越慢。为了解决这个问题，我们限制了并发请求的数量，在正在运行的请求任务完成之前，将剩余连接保存在队列中。

## 传统方法
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们如何实现爬虫的并发？一般情况下我们会创建一个线程池，每个线程通过一个套接字负责一个网页的下载。例如，从`xkcd.com`下载一个页面：
```python
def fetch(url: str) -> None:
	sock = socket.socket()  # 创建套接字对象
	sock.connect(("xkcd.com", 80))  # 与 xkcd.com 的80端口握手
	request = f'GET {url} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'  # 构建请求头
	sock.send(request.encode("ascii"))  # 发送数据
	response = b''  # 初始化响应
	chunk = sock.recv(4096)  # 每次接收 4096 b的数据
	# 循环接收，拼接响应
	while chunk:
		response += chunk
		chunk = sock.recv(4096)
   
	# 页面已经下载完
	links = parse_links(response)  # 解析页面，提取链接
	q.add(links)  # 队列中加入链接
```



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 默认情况下，套接字操作是*阻塞的*，当线程调用像`connect`或者`recv`方法时，线程在操作完成之前都会暂停。[^2]因此为了一次下载更多页面，我们需要更多的线程。一个复杂的应用通过在线程池中维护空余线程来分摊创建线程的开销，然后检查线程池，以便在下次任务中重复利用他们，与连接池中的套节字相同。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 然而，线程比较昂贵，操作系统对一个进程，用户或者机器拥有的线程数量有种种限制。在Jesse[^3]的系统中，一个Python线程大约消耗50k的内存，并且启动数万个线程时程序就会崩溃。如果我们扩展到对数万个套接字进行并发操作，在消耗完所有套接字之前，线程就消耗完了。每个线程的开销或者系统对线程的限制就是线程并发的瓶颈了。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 在他的知名文章"The C10K problem"[^4]中,Dan Kagel 概述了多线程对I/O并发的限制。他说到：

> 你不认为是时候网络服务器去解决同事处理一万个客户端的时候吗？毕竟，网站现在是一个巨大的容器。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Kegel 在1999年创造了"C10K"这个术语。一万个连接现在听起来比较简单，但是这个问题其实只改变了连接的数量大小，问题种类并没有发生改变。当时，C10K的每个连接都使用一个线程是不现实的。不过现在的单线程的连接数量限制上升了几个数量级。实际上，我们的玩具爬虫可以很好地使用线程工作。然而对于有数十万连接规模的超大型应用来说，上限依然存在：大多数系统即使可以继续创建套接字，但是也会耗尽所有线程。我们如何克服这个问题呢？

## 异步（Async）

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 异步I/O框架在单线程上使用*非阻塞*套接字完成并发操作。在我们的异步爬虫中，在套接字链接到服务器之前，我们将其设置为非阻塞式的，代码如下：

```python
sock = socket.socket()  # 创建套接字对象
sock.setbloking(False)  # 设置成非阻塞
try:
	sock.connect(("xkcd.com", 80))
except BlockingIOError:
  	pass
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 令人厌烦的是，即使工作正常，非阻塞套接字也会抛出连接异常。这个异常是复制了底层C语言函数的扰人行为，它将`errno`设置成`EINPROGRESS`告诉你（连接）已经开始了。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 现在我们的爬虫需要一个能够知道何时已经建立连接的方法，我们可以通过发送HTTP请求（来测试连接是否建立）。我们通过简单的while循环来实现：

```python
request = f"GET {url} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n"  # 最后两个\r\n代表请求头结束
encoded = request.encode("ascii")

while True:
    try:
        sock.send(encoded)  # 发送 HTTP 请求
        break  # 连接建立成功
    except OSError as e:
        pass

print("发送成功")
```



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 这个方法不仅费电，而且不能高效地在*多个*套接字上进行等待。以前，BSD Unix的解决方案是`select`, 一个 等待事件在非阻塞套接字上或者一个小的事件数组上发生的C 语言函数。如今，对于有大量连接的互联网应用的需求导致了（`select`）被例如`poll`，在BSD上的`kqueue`和在Linux上的`epoll`替换。这些接口都与`select`相似，但是在大量请求的情况下依然表现地很好。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Python3.4的`DefaultSelector`选择了在你的系统上可用的最佳的类`select`函数。为了注册关于网络`I/O`的通知，我们创建了一个非阻塞套接字并且使用默认`selector`注册它：

```python
from selectors import DefaultSelector, EVENT_WRITE

selector = DefaultSelector()  # 创建选择器对象

sock = socket.socket()
sock.setblocking(False)
try:
    sock.connect(("xdcd.com", 80))
except BlockingIOError:
    # 使用非阻塞必定抛出该异常
    pass

def connected() -> None:
    selector.unregister(sock.fileno())
	print("connected!")

selector.register(sock.fileno(), ENENT_WRITE, connected)  # 一个套接字会占用一个描述符，通过描述符来进行注册，事件（ENENT_WRITE）发生后，回调 connected 函数。
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 我们忽略掉假错误，调用`selector.register`, 传入套接字文件描述符和一个常量，该常量表示我们正在等待的事件。为了当连接可以用时得到通知，我们传入`EVENT_WRITE`：也就是说，我们想知道什么时候套接字是"可写的"。同时我们也传入了一个Python函数`connected`,以便在事件发生时运行。这样的函数就叫做`回调函数`。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 当选择器收到`I/O`通知时，我们在循环中进行处理：

```python
def loop() -> None:
    while True:
        events = selector.select()
        for event_key, event_mask in events:
            callback = envent_key.data
            callback()
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 回调函数`connected`被保存在`event_key.data`中，一旦非阻塞套接字连接完成，我们将读取并执行该回调函数。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 与之前的`while`循环不同（套接字循环发送代码段），当代码运行到`select`时会暂停，等待下一次的`I/O`事件。然后循环运行等待这些事件的回调完成。如果程序未完成将会一直挂起，直到事件循环中有新的通知。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 到目前为止我们已经展示了哪些呢？我们展示了如何开始注册事件并当事件准备就绪后执行回调函数。一个可以在单线程中运行并发操作的异步的框架就是构建于我们已经展示的两个特性（非阻塞套接字和事件循环）。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 我们在这里实现了"并发"，但是不是传统意义上的"并行"。也就是说我们构建了一个重叠I/O[^ 5]\(在Windows API 中被叫做异步I/O)的微型系统。它可以在其他操作正在进行时执行新的操作。实际上它并没有利用多核来执行并行计算。然而，这个系统为I/O密集型问题设计的，而不是为了计算密集型任务。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 因此，我们的事件循环对并发I/O的场景是很有效的，因为它没有分配线程资源给每个连接。但是在我们继续之前，必须纠正一个常见的误解，即异步比多线程更快。实际上，在Python中，像我们这样的事件循环在服务少量活跃连接的时候是比多线程稍慢的。在没有全局解释锁时，多线程能够表现的更好。异步`I/O`最适合的有很多慢、不活跃以及闲置的连接的应用[^6]。

## 回调编程

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 到目前为止，我们编写了一个很小的异步框架，但是我们如何才能编写一个网络爬虫呢？即使是简单的URL提取都很难下手。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 我们从创建尚未抓取的URL集合和浏览过的URL集合开始：

```python
urls_todo = set(["/"])
seen_urls = set(["/"])
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `seen_urls`集合包括`urls_todo`加上已经抓取过的URLs。这两个集合都用根URL`"/"`初始化。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 抓取一个页面需要一套回调函数。当套接字连接上时触发`connected`回调函数，然后给服务器发送一个`GET`请求。但是必须等待响应的返回，所以我们需要注册另一个回调函数。如果回调触发时，还不能读取所有响应，那就再次注册，以此类推。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 让我们把这些回调函数放进一个`Fetcher`对象。它需要一个`URL`、一个套接字对象和一个存放字节响应的地方：

```python
class Fetcher:
    def __init__(self, url: str) -> None:
        self.response = b""
        self.url = url
        self.sock = None
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 我们从调用`Fetcher.fetch`开始：

```python
	# Fetcher 类的方法
    def fetch(self) -> None:
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(("xkcd.com", 80))
        except BlockingIOError:
            pass
        
        # 注册下一步的回调
        selector.register(
            self.sock.fileno(),
            EVENT_WRITE,
            self.connected
        )
```



[^1]:  线程相关资源
[^2]: Even calls to `send` can block, if the recipient is slow to acknowledge outstanding messages and the system's buffer of outgoing data is full
[^3]: 原文作者之一
[^4]: http://www.kegel.com/c10k.html[↩](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html#fnref3)
[^ 5]: 原文叫做 `overlapping`I/O,详情请参考：[https://en.wikipedia.org/wiki/Overlapped_I/O](https://en.wikipedia.org/wiki/Overlapped_I/O)
[^6]: Jesse listed indications and contraindications for using async in ["What Is Async, How Does It Work, And When Should I Use It?":](http://pyvideo.org/video/2565/what-is-async-how-does-it-work-and-when-should). Mike Bayer compared the throughput of asyncio and multithreading for different workloads in ["Asynchronous Python and Databases":](http://techspot.zzzeek.org/2015/02/15/asynchronous-python-and-databases/)[↩](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html#fnref5)
