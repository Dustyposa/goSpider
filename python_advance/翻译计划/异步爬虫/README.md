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
sock.setblocking(False)  # 设置成非阻塞
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

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`fetch`方法始于连接到一个套接字。但是需要注意的是该方法在连接建立好之前已经返回了。它必须返回控制权给事件循环以便等待连接建立。至于为什么，假设我们整个应用的结构是这样的：

```python
# 开始抓取 http://xkcd.com/353/
fetcher = Fetcher("/353/")
fetcher.fetch()

while True:
    events = selector.select()
    for event_key, event_mask in events:
        callback = event_key.data
        callback(event_key, event_mask)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;当调用`select`方法时，所有事件通知都会在事件循环中处理。因此`fetch`必须将控制权给事件循环，以便程序知道什么时候套接字已经建立好连接了。只有这样，`while`循环才能回调在上述`fetch`方法结束时注册的`connected`函数，

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;以下是`connected`的实现：

```python
    # Fetcher 类的方法
    def connected(self, key, mask) -> None:
        print("connected!")
        selector.unregister(key.fd)
        request = f"GET {self.url} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n"
        self.sock.send(request.encode("ascii"))
        
        # 注册下一个回调函数
        selector.register(
            key.fd,
            EVENT_READ,
            self.read_response
        )
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 该方法发送一个`GET`请求。不过一个真正的应用是需要检查`send`的返回值（译者注：`send`函数的返回值表示成功发送的字节数），以防止没有一次性发送完所有数据。但是我们的请求信息比较少，而且我们的程序也很简单。直接调用`send`，然后等待响应的返回。当然，程序必须注册另一个回调函数并把控制权交回事件循环。下一个也是最后一个回调函数，`read_response`,处理服务器的回应：

```python
    # Fetcher 类的方法
    def read_response(self, key, mask) -> None:
        global stopped

        chunk = self.sock.recv(4096)  # 每块 4K 大小
        if chunk:
            self.reponse += chunk
        else:
            selector.unregister(key.fd)  # 读取响应完成
            links = self.parse_links()

            # Python 集合处理逻辑
            for link in links.difference(seen_urls):
                urls_todo.add(link)  
                Fetcher(link).fetch()   # 创建新的 Fetcher

            seen_urls.update(links)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped = True
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 每当`selector`检测到套接字可读时（"可读"可能意味着两件事：套接字有收到数据了或者已经关闭了）就会执行该回调函数。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 该回调需要从套接字获取4k的数据。如果数据不够，不论数据是否可用`chunk`都会阻塞。如果数据足够的话，`chunk`就有4k长度并且套接字也会保留可读性，所以事件循环在下一次收到通知时，会再次执行该回调函数。当全部响应读取完成时，目标服务器就会关闭套接字，并且`chunk`就没有数据了。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 未展示的`parse_links`方法返回值是一个`URL`的集合。我们为每个新`URL`都创建了一个`fetcher`，这里没有并发上限。注意，用回调进行异步编程的有一个优势就是：即使对公共数据进行写操作我们也不需要互斥锁，例如在我们向`seen_urls`添加链接时。因为不是抢占式多任务，所以我们的代码在任何位置都不能被中断[^7]。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 我们添加一个全局变量`stopped`用来控制循环：

```python
stoped = False
def loop() -> None:
    while not stoped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;一旦所有页面抓取完成，`fetcher`就让全局的事件循环停止并退出程序。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这个例子反映出了异步编程的一个典型的问题：面条式代码。我们需要某种方式来表示一系列的计算和I/O操作，并调度多个此类操作让他们并发执行。但是没有了线程，这一系列的操作都不能写到同一个函数中：只要函数开始进行一个I/O操作，它都需要显示地保存将来需要处理的任何状态（译者注：例如可读、可写等），然后返回。你需要自己思考和编写这个状态保存的代码。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;让我们解释一下上面说的到底是什么意思。先看一下在一个线程中使用传统的阻塞套接字抓取一个链接有多简单：

```python
# 阻塞版本 
def fetch(url: str) -> None:
    sock = socket.socket()
    sock.connect(('xkcd.com', 80))
    request = f'GET {url} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        chunk = sock.recv(4096)

    # 页面下载完成
    links = parse_links(response)
    q.add(links)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在一次套接字操作和下一次操作之间，函数记录了什么状态呢？它有一个套接字对象，一个URL和可增长的`response`。运行在线程的中的函数利用编程语言的基础特性将临时变量保存在其堆栈的局部变量中。该函数也有一个“continuation（延伸）“——即计划在I/O完成后执行的代码。运行时通过保存线程的指令指针来记住这个 continuation 部分。你不需要考虑在I/O完成后如何恢复这些局部变量以及 contination 部分。语言本身的特性就帮你解决了。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;但是对于基于回调的异步框架，这些语言特性是没有任何帮助的。只要在等待I/O，函数必须显示保存它的状态，因为一旦函数在I/O完成之前就会返回，并且会丢失堆栈帧。在之前的回调示例中，作为局部变量的替代，我们把`sock`和`response`作为`Fetcher`实例化后的`self`的属性来保存。为了替代指令指针，通过注册`connected`和`read_reponse`回调函数来保存它的 continuation 。由此可见，随着应用功能的增加，我们手动保存回调状态的复杂性也在增加。如此繁杂的记账式工作让程序员很头痛。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;更糟糕的是，在一次回调和下一次回调之间抛出异常会发生什么？假设我们`parse_links`方法写的很差，在解析某些HTML时抛出了异常：

```python
Traceback (most recent call last):
  File "loop-with-callbacks.py", line 111, in <module>
    loop()
  File "loop-with-callbacks.py", line 106, in loop
    callback(event_key, event_mask)
  File "loop-with-callbacks.py", line 51, in read_response
    links = self.parse_links()
  File "loop-with-callbacks.py", line 67, in parse_links
    raise Exception('parse error')
Exception: parse error
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;栈回溯信息只能展示事件循环正在运行一个回调函数。我们不知道是什么导致了错误。回调链的两端都被破坏了，不知道从哪开始从哪结束。这种上下文丢失的情况叫做“堆栈撕裂（stack ripping）”，在很多情况下都会让我们束手无策。堆栈撕裂还会阻止我们为回调链设置异常处理，即通过“`try/except`”块封装函数调用及其调用树[^8]。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;因此，除了关于多线程和异步谁的运行效率更高的争论以外，还有一个关于哪个更容易出错的争论：如果在同步时失误，线程更容易受到数据争夺（译者注：公有数据，线程的同步与互斥问题。）的影响，但是回调发生堆栈撕裂时，调试会变得令人痛苦不堪。

## 协程（Coroutines）

> 译者注：下面这部分的代码比较老了，因为python34还没有 `await` `async` 这类东西，用的原始的 `yiled from` 实现的协程。以下部分可以当做原理了解，项目实操中请不要使用，请用最新写法，推荐py37+版本。后面计划出最新的`python`协程教程，敬请期待。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 我们向你保证。编写高效回调与多线程编程简单的代码风格相结合的异步代码也是没有问题的（译者注：py37+更简单了！）。这种结合是通过一种叫“协程（coroutines）”的模式实现的。使用Python3.4的`asyncio`标准库和叫做`aiohttp`的第三方库，在协程中抓取一个URL就很简单了[^9]:

```python
    @asyncio.coroutine
    def fetch(self, url):
        response = yield from self.session.get(url)
        body = yield from response.read()
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 当然，代码的可扩展性也是没有问题的。与每个线程需要`50k`内存和操作系统对其有硬限制的多线程相比，一个`python 协程`在 Jesse的系统上仅仅需要`3k`的内存。python 可以轻轻松松地开启成千上万个协程。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 协程的概念可以追溯到计算机科学的早期，也很简单：一个可暂停和继续的例程（译者注：[协程的子集]( https://en.wikipedia.org/wiki/Coroutine#Comparison_with_subroutines )）。多线程是抢占式的的，并发优先级是由操作系统控制，但是协程是协作式的：由自身选择什么时候暂停，什么时候运行下一个协程。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 协程有很多的实现方式，即使在python中也有几种实现方式（译者注：最著名的例如：`gevent`三方库和`asynico`标准库 ，实现方式就不同）。Python3.4中的标注库`asynico`中的协程是基于生成器，`Future`类和`yield from` 语句构建的。从 Python3.5 开始，协程就是语言的一个原生特性了[^8]。但是，了解最初在在Python3.4中使用现存的语言工具实现的协程，是在Python3.5中实现原生协程的基础。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 为了解释Python3.4中基于生成器实现的协程，我们将介绍生成器以及在它如何在`asyncio`中作为协程使用。相信你你阅读如我写书这般享受。在解释完基于生成器实现的协程之后，我们将异步网络爬虫中使用协程。

## Python 生成器是如何工作的

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 在你掌握**Python**生成器之前，你需要去了解正常的**Python**函数如何工作的。正常情况下，当`Python`函数调用一个子例程(subroutine)时，子例程在函数返回或者抛出异常之前会保留控制权。之后将郭志全返回给调用者：

```python
>>> def foo():
...     bar()
...
>>> def bar():
...     pass
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 标准的**Python**解释器使用**C**写的。执行**Python**函数的**C**函数被统称为`PyEval_EvalFrameEx`。它接收一`Python栈帧对象`并在框架上下文中计算`Python字节码`。下面是`foo`的字节码：

```python
>>> import dis
>>> dis.dis(foo)
  5           0 LOAD_GLOBAL              0 (bar)
              2 CALL_FUNCTION            0
              4 POP_TOP
              6 LOAD_CONST               0 (None)
              8 RETURN_VALUE
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `foo`函数将`bar`加载到堆栈上，并调用它，然后从堆栈中弹出它的返回值，将`None`加载到堆栈上，最后返回`None`。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 当`PyEval_EvalFrameEx`碰到`CALL_FUNCTION`字节码时，它会新建一个`Python 栈帧`并递归：也就是说，它用一个新的帧递归地调用`PyEval_EvalFrameEx`，该帧用来执行`bar`。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 理解`Pthon栈帧`是堆内存分配这件事是极其重要的！`Python`解释器是一个普通的C程序，所以他的栈帧也是普通的栈帧。但是它操作的`Python栈帧`在堆上。出乎意料的是，这意味着一个`Python栈帧`可以比它的函数调用存在更久。要想看交互式的效果，在`bar`中保存当前帧：

```python
>>> import inspect
>>> frame = None
>>> def foo():
...     bar()
...
>>> def bar():
...     global frame
...     frame = inspect.currentframe()
...
>>> foo()
>>> # 帧正在执行 'bar' 的代码
>>> frame.f_code.co_name
'bar'
>>> # 下一个帧指向的为'foo'
>>> caller_frame = frame.f_back
>>> caller_frame.f_code.co_name
'foo'
```



![function-calls.png](https://i.loli.net/2019/11/13/siMN7VcqEPIfAuU.png)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  Figure 5.1 - Function Calls 

现在为`Python生成器`设置好了同样的阶段，使用相同的构建块——代码对象和栈帧——得到了很好的效果。

这是一个生成器函数：

```python
>>> def gen_fn():
... 	result = yield 1
... 	print(f'result of yield: {result}')
... 	result2 = yield 2
... 	print(f'result of 2nd yield: {result2}')
... 	return 'done'
... 
```

当`Python`将`gen_fn`编译为字节码时，编译器看到`yield`声明就知道`gen_fn`是一个生成器函数，不是一个常规的函数。它会设置一个`flag`去记住这个事实：

```python
>>> # 生成器标志是 5比特位(bit position 5)
>>> generator_bit = 1 << 5
>>> bool(gen_fn.__code__co_flags & generator_bit)
True
```

当你调用一个生成器函数时，`Python`看见生成器`flag`并不会真的运行这个函数。反而它会创建一个生成器：

```python
>>> gen = gen_fn()
>>> type(gen)
<class 'generator'>
```

`Python`生成器封装了一个栈帧和一个对某些代码的引用，`gen_fn`的主体:

```python
>>> gen.gi_code.co_name
'gen_fn'
```

从对`gen_fn`的调用到所有的生成器都指向相同的代码。但是每个都有自己的栈帧。这个栈帧不在任何真实的栈上面，它在堆内存中等待被使用：

![generator.png](https://i.loli.net/2019/11/13/lEUd6p8Doz4ZrSh.png)

这个帧有一个“最后的指令”指针，就是它最近执行的指令。在刚开始的时候，最后的指令指针为`-1`，意味着生成器还没开始：

```python
>>> gen.gi_frame.f_lasti
-1
```

当我们调用`send`的时候，生成器到达第一个`yield`并暂停。`send`的返回值是`1`，这是由`gen`通过`yield`表达式传递的：

```python
>>> gen.send(None)
1
```

生成器指令指针现在是3字节码，部分通过编译的`Python`有56字节：

```python
>>> gen.gi_frame.f_lasti
3
>>> len(gen.gi_code.co_code)
56
```

生成器可以在任何时候从任何函数复位(resumed)，因为它的栈帧并没有真正的存在栈上：它在堆上。它在调用层次结构中位置是不固定的，并且它不需要遵循常规函数执行时的先进后出的顺序。它是自由的，像自由漂浮的云。

我们可以给生成器发送`hello`，它会成为`yield`表达式的结果，生成器继续运行只到它`yields 2`:

```python
>>> gen.send('hello')
retult of yield: hello
2
```

它的栈帧现在有了局部变量`result`:

```python
>>> gen.gi_frame.f_locals
{'result': 'hello'}
```

从`gen_fn`创建的其他生成器有它们自己的栈帧和局部变量。

我们可以再次调用`send`，生成器继续运行直到遇到第二个`yield`，在抛出一个特殊的`StopIteration`错误后结束掉。

```python
>>> gen.send('goodbye')
result of 2nd yield: goodbye
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration: done
```

这个异常有一个值，就是作为生成器返回的值：字符串"done".

## 用生成器构建协程

因此，一个生成器可以暂停，用一个值可以恢复并且有一个返回值。这听起来很好的原始方法去构建一个异步编程模型，并且不需要复杂(`spaghetti`)的回调！我们想去构建一个`"coroutine"`:一个可以和其他的例程在程序中协同调度的例程。我们的协程将是`Python`标准库`"asynico"`库中的那些协程的简化版本。跟`asyncio`中的一样，我们将使用`generators,futures,and 'yield from'语法`。

首先，我们需要一种方式来表示协程正在等待的一些`futrue`结果。一个精简版:

```python
class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []
    
    def add_done_callback(self, fn: Callable) -> None:
        self._callbacks.append(fn)
    
    def set_result(self, result) -> None:
        self.result = result
        for fn in self._callbacks:
            fn(self)
        
```

一个`future`刚开始是`pending`状态。通过调用`set_result`[^11]变为`"resolved"`状态。

让我们调整我们的`fetcher`，使用`futures and coroutines`.我们用回调编写`fetch`。

```python
class Fetcher:
    def fetch(self) -> None:
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(("xkcd.com", 80))
        except BlockingIOError:
            pass
        selector.register(
            self.sock.fileno(),
            EVENT_WRITE,
            self.connected
        )
        
    def connected(self, key, mask) -> None:
        print('connected!')
        # And so on....
```



`fetch`方法开始连接一个`socket`,然后注册回调，`connected`,当`socket`准备好后回调会被执行。现在我们可将这两倍结合到一个协程中：

```python
def fetch(self) -> Generator:
    self.sock = socket.socket()
    self.sock.setblocking(False)
    try:
        self.sock.connect(('baidu.com', 80))
    except BlockingIOError:
        pass
    f = Future()
    
    def on_connected():
        f.set_result(None)
        
    selector.register(
        self.sock.fileno(),
        EVENT_WRITE,
        on_connected
    )
    yield f
    
    selector.unregister(self.sock.fileno())
```

现在,`fetch`是一个生成器函数，并不是常规的函数，因为它包含了`yield`语句。我们创建了一个`pending`状态的`future`,然后`yield`它去暂停`fetch`直到`socket`准备好。内部函数`on_connected`将会`resolves future`。

但是当`future resolves`时，怎么恢复生成器呢？我们需要一个协程掌舵者(`driver`).让我们叫它`task`:

```python
class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future: Future) -> None:
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return

        next_future.add_done_callback(self.step)


# 开始抓取 http://xkcd.com/353
fetcher = Fetcher('/353/')
Task(fetcher.fetch())

loop()

```

`taak`通过发送`None`给`fetch`生成器来启动它。然后`fetch`开始运行直到`yields`一个`future`,它回被`task`被当作`next_future`捕获。当`socket`建立连接成功后，事件循环会运行回调函数`on_connected`，来释放`future`，`future`将会调用`step`,从而恢复`fetch`。

## 用`yield from`代理协程

一旦`socket`建立连接成功，我们就发送`HTTP GET`请求并读取服务器的响应。这些步骤不需要分散在回调函数之间；我们将它们放到同一生成器函数中：

```python
    def fetch(self) -> Generator:
        # ... 连接逻辑同上，然后：
        self.sock.send(request.encode('ascii'))

        while True:
            f = Future()

            def on_readable():
                f.set_result(self.sock.recv(4096))

            selector.register(
                self.sock.fileno(),
                EVENT_READ,
                on_readable
            )

            chunk = yield f
            selector.unregister(self.sock.fileno())
            if chunk:
                self.response += chunk
            else:
                # 响应读取完成
                break
```

>  *译者注： 这里网络状况问题比较多，建议配合译者的响应代码文件食用，尽量测试客户端连接本地服务器，不然结果会有一些不尽人意。*

这段代码，会从`socket`中读取整个信息，通常看起来很有用。我们如何把它从`fetch`中分解成一个子例程呢？现在`Python 3`有名的`yield from`登场了。它把一个生成器委托给了另一个。

为了了解如何操作，让我们回到一个简单的生成器例子:

```python
>>> def gen_fn():
...     result = yield 1
...     print(f'result of yield: {result}')
...     result2 = yield 2
...     print(f'result of 2nd yield: {result2}')
...     return 'done'
... 
```

为了从另一个生成器中调用这个生成器，用`yield from`进行委托。

```python
>>> # 生成器函数
>>> def caller_fn():
...     gen = gen_fn()
...     rv = yield from gen
...     print(f'return value of yield-from: {rv}')
...     
>>> # 从生成器函数生成一个生成器
>>> caller = caller_fn()
```

`caller`生成器的行为和`gen`相似，生成器委托给了：

```python
>>> caller.send(None)
1
>>> caller.gi_frame.f_lasti
15
>>> caller.send('hello')
result of yield: hello
2
>>> caller.gi_frame.f_lasti  # 未增加
15
>>> caller.send('goodbye')
result of 2nd yield: goodbye
return value of yield-from: done
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration
```

当`caller yields from gen`时，`caller`没有增加*(指针)*[^12]。请注意，即使内部的生成器`gen`从一个`yield`语句运行到下一个`yield`语句，它的指针也保持在 15，即声明`yield from`的位置。从外部`caller`的角度来看，我们不能够判断它`yield`的值来自`caller`还是来自它委托的生成器。从内部的`gen`来看，我们不能判断发送的值是来自`caller`或者来自它的外部。`yield from`语句是一个流畅的通道，在`gen`结束之前，值通过它出入`gen`。

一个协程可以用`yield from`将工作委托给一个子协程，并接收子协程工作的结果。需要注意的是，在上面的代码中，`caller`打印了`"return value of yield-from: done"`。当`gen`执行完成时，它返回的值成为了`caller`中 `yield from` 语句产生的值：

```python
	rv = yield from gen
```

之前，在我们批评基于回调的异步编程的时候，我们最突出的抱怨是关于`"stack ripping"`的：当一个回调抛出一个异常时，堆栈追踪通常是无用的。它仅仅展示了时间循环正在运行回调，而不是*原因*。那么协程怎么样？

```python
>>> def gen_fn():
...     raise Exception('my error')
>>> caller = caller_fn()
>>> caller.send(None)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "<input>", line 3, in caller_fn
  File "<input>", line 2, in gen_fn
Exception: my error
```

这就有用多了！堆栈追踪展示了当异常抛出时，`caller_fn`正在委托`gen_fn`。更令人欣慰的是，我们可以把对子协程的调用封装在异常处理中，这和普通的子例程相同：

```python
>>> def gen_fn():
...     yield 1
...     raise Exception('uh oh')
...
>>> def caller_fn():
...     try:
...         yield from gen_fn()
...     except Exception as exc:
...         print(f'caught {exc}')
...
>>> caller = caller_fn()
>>> caller.send(None)
1
>>> caller.send('hello')
caught uh oh
```

所以，就像常规的子例程一样，我们分解一下子协程程的逻辑。让我们从我们的`fetcher`中分解一些有用的子协程。我们写一个`read`写成来接收一个`chunk`:

```python
def read(sock: socket.socket):
    f = Future()

    def on_readable():
        f.set_result(sock.recv(4096))

    selector.register(
        sock.fileno(),
        EVENT_READ,
        on_readable
    )
    chunk = yield f  # 读一个chunk
    selector.unregister(sock.fileno())
    return chunk
```

我们在`read`的基础上构建一个`read_all`协程，用于接收整个消息：

```python
def read_all(sock: socket.socket):
    response = []
    # 读取所有消息
    chunk = yield from read(sock)
    while chunk:
        response.append(chunk)
        chunk = yield from read(sock)

    return b''.join(response)
```

如果你以正确的方式换角度看的话，`yield from`语句就会消失，并且这些语句看起来和常规的函数一样，会阻塞`I/O`。但实际上，`read`和`read_all`都是协程。`yield from read`会暂停 `read_all`直到所有的`I/O`完成。当`reda_all`暂停时，`asyncio`的事件循环会执行其他的工作并等待(awiat)其他的`I/O`事件；一旦事件就绪，`read_all`就会在下一个循环中恢复并获得`read`的结果。

在堆栈的根*(此处指 __main__ 的全局空间)*，`fecth`调用`read_all`:

```python
class Fetcher:
    def fetch(self) -> Generator:
        # ... 连接逻辑同上，然后：
        self.sock.send(request.encode('ascii'))
        self.response = yield from read_all(self.sock)
```

令人惊喜的是，`Task`类不需要做任何修改。它和以前一样，驱动外部的`fetch`协程就行：

```python
Task(fetcher.fetch())
loop()
```

当然`read` yield 一个`future` 时，`task`通过`yield from`语句的通道接收它，就像`future`是直接从`fetch`中产生*(yielded)*的一样。当循环释放一个`future`时，`task`把结果发送到了`fetch`，并且通过`read`直接把值接收了，就像`task`直接在驱动`read`:

![figure_yield](http://aosabook.org/en/500L/crawler-images/yield-from.png)

​																				Figure 5.3 - Yield From  

为了完善我们的协程实现，我们改进了一个标记：当它等待一个`future`时，我们的代码使用的`yield`，当它委托给一个子协程时，使用的`yield from`。如果我们在协程暂停时使用`yield from`，效果会更好。那么洗成就不需要关注它等待的东西是什么类型。

我们利用了`Python`中生成器和迭代器的深度对应关系。对于调用者来说，推进的生成器和推进的迭代器都是一样的。所以我们让我们的`Future`类通过一个特殊的方法实现可迭代：

```PYTHON
    # Future 类的方法
    def __iter__(self):
        # 告诉 Task 在这里继续
        yield self
        return self.result
```

`future`的`__iter__`方法是一个`yields future 自身`的协程。现在当我们像这样替换代码时:

```python
# f is a Future.
yield f
```

...用这样的代码进行替换：

```python
# f is a Future.
yield from f
```

...结果是一样的！驱动器`Task`调用`send`收到`future`,并且当`future`结束时，它会将新的结果发送回协程。

到处都使用`yield from`的好处是什么？为什么比用`yield`等待`future`以及用`yield`委托给子协程好？好的原因是因为现在，一个方法可以自由的改变实现而不影响调用者：它可以是一个常规的函数，返回一个`future`然后将会`resolve`一个值，或者它也可以是一个协程，包含了`yield from`语句并`returns`一个值。在这两种情况下，调用者都只需要`yield from`去等待结果。

读者们，我们已经愉快的完成了对在`asyncio`中协程的阐述。我们探究了生成器的机制，并勾画实现了`futures and tasks`。我们概述了异步是如何取得这两方面的最佳效果的:并发I/O比线程更有效，比回调更清晰。当然，真正的`asyncio`是比我们简述版复杂的多的。真正的框架实现了零拷贝`I/O`,平衡调度，异常处理和大量的其他功能。

对于一个`asyncio`用户来说，用协程编程比你在这里看到的简单多。在上面的代码中，我们从基本原理开始实现协程，所以你看到了回调，`tasks and futures`。甚至你看见了非阻塞的`socket`和`select`调用。但是当需要用`asyncio`构建应用的时候，这些都不会出现在你的代码里。如我们所承诺的，你现在可以轻松抓取一个`URL`：

```python
    @asyncio.coroutine
        def fetch(self, url):
            response = yield from self.session.get(url)
            body = yield from response.read()
```

满足于此，我们回到了最初的任务:使用`asyncio`编写一个异步`web`爬虫。



## 整合协程

我们首先描述了我们希望爬虫如何工作。现在，是时候去用`asyncio 协程`实现它了。

我们的爬虫将抓取第一个页面，解析它的链接，并把它们加入一个队列。之后，它会散布在整个网站上，并发抓取页面。但是为了限制客户端和服务器的负载，我们希望有一些最大运行数量的`works`，而不是无限多。当一个`worker`抓取到一个页面，它应该立即从队列中`pull`下一个链接。我们将会经历一段没有足够的工作去做的时期，所以一些`workers`必须暂停。但是当一个`worker`点击一个有很多新链接的页面时，队列会突然增加，并且任何暂停的`workers`都应该苏醒并开始工作。最后，一旦`work`结束，我们的程序必须退出。

想象一下，如果这些`workers`是线程们。我们怎样才能表达这个爬虫算法？我们需要使用一个`Python`标准库中的同步队列[^13]。每当一个`item`放入队列，队列就会增加`"tasks"`的计数。工作线程在完成一个`item`工作后调用`task_done`。主线程将会阻塞在`Queue.join`直到每个放到队列中`item`被`task_done`调用匹配，然后退出。

协程与`asyncio`队列使用完全相同的模式！ 首先我们导入它：

```python
try:
    from asyncio import JoinableQueue as Queue
except ImportError:
    # 在 Python 3.5，asyncio.JoinableQueue 并入到了 Queue
    from asyncio import Queue
```

我们在一个`crawler`类中收集`workers`的共享状态，并将主要逻辑写在`crawl`方法中。我们在一个协程中启动`crawl`并运行`asyncio`时间循环，直到`crawl`结束：

```python
loop = asyncio.get_event_loop()

crawler = crawling.Crawler('http://xkcd.com',
                           max_redirect=10)

loop.run_until_complete(crawler.crawl())
```

`crawler`从一个根`URL`和`max_reirect`开始，抓取任何一个`URL`时都会遵循`redirects`的次数。它会把`(URL, max_redirect)`成对放入队列中（至于原因，请继续关注）。

```python
class Crawler:
    def __init__(self, root_url: str, max_redirect: int):
        self.max_tasks = 10
        self.max_redirect = max_redirect
        self.q = Queue()
        self.seen_urls = set()

        # aiohttp 的 ClientSession 执行连接池 并且 HTTP 为我们 keep-alive
        self.session = aiohttp.ClientSession(loop=loop)

        # 把 (URL, max_redirect) 放入队列
        self.q.put((root_url, self.max_redirect))
```

没有完成的`tasks`数量现在只有一个。回到我们的主脚本，我们运行事件循环和`crawl`方法：

```python
loop.run_until_complete(crawler.crawl())
```

`crawl`协程让`workers`开始工作。看起来像一个主线程：它阻塞在`join`直到所有的任务结束，而`workers`在后台运行。

```python
    @asyncio.coroutine
    def crawl(self):
        """运行 crawler 直到所有的工作完成"""
        wokers = [asyncio.Task(self.work())
                  for _ in range(self.max_tasks)]

        # 当所有任务完成，退出
        yield from self.q.join()
        for w in wokers:
            w.cancel()
```

如果我们的`workers`是线程，我们可能并不希望他们在同一时刻开始。为了在确定需要其他线程之前避免创建昂贵的线程，线程池通常需要按需增长。但是协程很廉价，所以我们简单的在开始设置最大数目即可。

值得注意的是我们如何关闭`crawler`的。当`join`的`future`释放时*（resolve）*，`worker`的任务还存在但是已经暂停了：它们等着更多的`URLs`但是还没有到来。所以，主协程在退出之前取消掉它们。否则，当`Python`解释器关闭并调用所有对象的析构函数时，正在运行的任务会提示到：

```
ERROR:asyncio:Task was destroyed but it is pending!
```

那么我们如何`cancel`工作？生成器有一个特性我们还没有给你展示过。你可以从外面向生成器里面抛出一个异常。

```python
>>> gen = gen_fn()
>>> gen.send(None)  # 和往常一样启动生成器。
1
>>> gen.throw(Exception('error'))
Traceback (most recent call last):
  File "<input>", line 3, in <module>
  File "<input>", line 2, in gen_fn
Exception: error
```

生成器由`throw`恢复，但是它现在引出了一个异常。如果没有代码在生成器的调用栈中捕获异常，该异常会冒泡回到栈顶。所以去取消一个`task`的协程：

```python
  # Task 类的方法  
  def cancel(self):
        self.coro.throw(CancelledError)
     
```

不论生成器在哪里暂停，在某个`yield from`语句，它都会恢复并抛出一个异常。我们在`task`的`step`方法中处理该取消：

```python
  # Task 类的方法  
  def step(self, future: Future) -> None:
        try:
            next_future = self.coro.send(future.result)
        except CancelledError:
            self.cancelled = True
            return 
        except StopIteration:
            return

        next_future.add_done_callback(self.step)
```

现在`task`知道它被取消了，所以当它被摧毁时，它不会对看不到光芒而愤怒。

一旦`crawl`已经取消了`workers`，它会退出。事件循环看见协程结束了*（之后我们再看）*，它也会退出。

```
loop.run_until_complete(crawler.crawl())
```

`crawl`方法包含了所有我们主协程必须做的事。从队列中获取`URLs`，抓取和解析新链接是`worker`协程做的事情。每个`worker`都会独立的运行`work`协程：

```python
    @asyncio.coroutine
    def work(self):
        while True:
            url, max_redirect = yield from self.q.get()

            # 下载页面并向 self.q 中增加新链接
            yield from self.fetch(url, max_redirect)
            self.q.task_done()

```

`Python`发现代码中包含`yield from`语句，将其编译成生成器函数。所以在`crawl`中，当主协程调用`self.work`10次，它不会真正的执行函数：它仅仅创建了10个引用这段代码的生成器对象。它会封装每个`Task`.`Task`每次收到生成`yields`的`future`，当`future resolves`时，就会通过调用每个带有`future`结果的`send`来驱动该生成器。因为每个生成器都有它们自己的栈帧，它们运行独立，有隔离的局部变量及程序计数器。

`worker`通过队列和伙伴们协调。等待新的`URL`:

```python
    url, max_redirect = yield from self.q.get()
```

队列的`get`方法本身就是一个协程：在有人放一个`item`到队列中之前都是暂停的，之后就会恢复并返回`item`。

顺便说一句，当主协程取消它时，这个地方就是在`crawl`的最后被暂停的位置。以协程的角度来看，当`yield from`引出一个`CancelledError`异常时，最后一次循环就结束了。

当一个`worker`抓取一个页面时，解析链接并向队列中放入新的链接，之后调用`task_done`并递减计数器。最终，一个`worker`抓取一个其`URLs`已被全部抓取的页面，并且队列中也没有剩余的`work`。因此，`workers`调用`task_done`计数器递减至0。在这之后正在等待队列的`join`方法的`crwal`将不再暂停并结束运行。

我们答应了解释为什么放入队列的`items`为什么是一对，就像：

```python
# 去抓取的 URL， 剩余重定向的次数
('http://xkcd.com/353', 10)
```

新的`URLs`有10次重定向次数。获取这个特定的`URL`将导致重定向到一个后面带有斜杠的新位置。我们递减保留的重定向数目，并将下一个地址放入队列中：

```python
# 末尾有斜杠的 URL, 剩余9次重定向
('http://xkcd.com/353/', 9)
```

我们使用的`aiohttp`包默认的会遵循重定向并给我们最后的响应。但是，我们告诉它不要这样做，在`crawler`中处理重定向，所以这样就可以合并指向相同位置的重定向地址：如果是我们抓取过这个`URL`，它会在`self.seen_urls`中并且我们也从不同的入口点开始了：

![Redirects](http://aosabook.org/en/500L/crawler-images/redirects.png)

​																				*Figure 5.4 - Redirects*

`crawler`抓取`"foo"`并看到了它重定向到`"baz"`，所以它将`"baz"`加进队列和`seen_urls`。如果下个页面抓取的是同样会重定向到`"baz"`的`"bar"`，`fetcher`不会再将`"baz"`入队。如果响应是一个页面，而不是重定向，`fetch`会解析页面的链接并将新的链接放入队列。

```python
    @asyncio.coroutine
    def fetch(self, url: str, max_redirect: int):
        # 我们自己处理 redirects
        response = yield from self.session.get(
            url, allow_redirects=False
        )

        try:
            if is_redirect(response):
                if max_redirect > 0:
                    next_url = response.headers['location']
                    if next_url in self.seen_urls:
                        # 我们已经下载过这个路径
                        return

                # 记录我们已经看过这条连接
                self.seen_urls.add(next_url)

                # 跟进重定向，重定向次数减一
                self.q.put_nowait((next_url, max_redirect - 1))
            else:
                links = yield from self.parse_links(response)
                # python集合逻辑
                for link in links.dirrerence(self.seen_urls):
                    self.q.put_nowait((link, self.max_redirect))
                self.seen_urls.update(links)
        finally:
            # 返回连接池
            yield from response.release()
```

如果这是多线程的代码，则竞争条件会很糟糕。比如说，`woker`检查一个链接是否在`seen_urls`中时，如果不在，`worker`将会把链接放入队列并加入`seen_urls`。如果在两次操作中间被打断，然后另一个`worker`可能从一个不同的页面解析到同样的链接，也需要检查它不是不是不在`seen_urls`中，并且也需要把它加入队列。那么现在同样的链接将会在队列中出现两次，导致（最好的情况下）重复工作和错误的统计信息。

然而，一个协程只会在有`yield from`语句时容易中断。这就是一个关键区别，使得协程代码比多线程代码更不容易出现竞争：多线程代码必须利用锁来显示的进入临界部分，否则它是可以中断的。一个`Python`协程默认情况下是不可中断的，只有当它显式的`yields`时才会放弃控制。

我们不再需要一个像我们基于回调的程序中的`fetcher`类。该`class`是一个缺少回调的解决办法：当在等待`I/O`时他们需要一些位置来存储状态，因为它们的局部变量是不会在回调之间保留。但是`fetch`协程可以与常规函数一样在局部变量中保存状态，所以这里不再需要一个`class`。

当`fetch`处理完`server`的响应时，它会返回给调用方`work`。`work`方法调用队列的`task_done`方法，然后从队列中获取到下一个要被抓取的`URL`。

当`fetch`放入一个新的链接到队列时，它会增加未完成的`tasks`的数量，并使在等待`q.join`的主协程暂停。但是，如果没有未抓取过的链接，该链接就是队列中的最后一个链接，在`work`调用`task_done`之后，未完成的`tasks`的数量将会降为0。该事件将会不再暂停`join`，主协程完成。

协调`workers`和主协程的队列代码就像这样[^14]：

```python
import asyncio


class Queue:
    def __init__(self):
        self._join_future = Future()
        self._unfinished_tasks = 0
        # ... 其他的初始条件

    def put_nowait(self, item):
        self._unfinished_tasks += 1
        # ... 保存 item

    def task_done(self):
        self._unfinished_tasks -= 1
        if self._unfinished_tasks == 0:
            self._join_future.set_result(None)

    @asyncio.coroutine
    def join(self):
        if self._unfinished_tasks > 0:
            yield from self._join_future

```

主协程`crawl`，`yields from` `join`。所有当最后一个`worker`将减少未完成的`tasks`的数量减少至`0`的时候，就标志着`crawl`恢复并结束。

旅程快结束了。我们的程序以调用`crawl`开始：

```
loop.run_until_complete(self.crawler.crawl())
```

程序怎么结束的呢？因为`crawl`是一个生成器函数，调用之后返回一个生成器。为了驱动生成器，`asyncio`封装了一个`task`:

```python
class EventLoop:
    def run_until_complete(self, coro):
        """运行直到生成器结束"""
        task = Task(coro)
        task.task_done_callback(stop_callback)
        try:
            self.run_forever()
        except StopError：
            pass


class StopError(BaseException):
    """抛出停止事件循环"""


def stop_callback(future):
    raise StopError

```

当`task`结束，它会引发作为循环使用的作为正常结束的信号`StopError`。

但是这是什么？`task`有一个叫做`add_done_callback`的方法和`result`？你可能会认为`task`就像`future`。你的直觉是对的。我们必须承认一个我们向你隐藏的`Task类`的细节：`task`就是`future`。

```python
class Task(Future):
    """封装在 Future 的协程"""
```

正常情况下，一个`future`被某些其他调用自己的`set_result resolves`。但是当协程停止时，`task resolves`*自己*。请记住，在我们直接对`Python生成器的`探索中，当一个生成器`return`时，它会引发一个特殊的`StopIteration`异常：

```python
    def step(self, future: Future) -> None:
        try:
            next_future = self.coro.send(future.result)
        except CancelledError:
            self.cancelled = True
            return
        except StopIteration as exc:

            # Task 用 coro's 返回值 resolves 自己 
            self.set_result(exc.value)
            return

        next_future.add_done_callback(self.step)
```

所以当事件循环调用`task.add_done_callback(stop_callback)`时，它就准备被`task`停止。这里再一次的`run_until_complete`：

```python
    def run_until_complete(self, coro):
        """运行直到生成器结束"""
        task = Task(coro)
        task.task_done_callback(stop_callback)
        try:
            self.run_forever()
        except StopError:
            pass
```

当`task`捕获到`StopIteration`并`resolves`自己，回调在循环中引发`StopError`。循环停止，调用堆栈退回到`run_until_complete`。 我们的程序结束了。

## 结论

现代程序越来越经常受`I / O`约束，而不是受`CPU`约束。对于这样的程序，`Python`线程在这些领域是很糟糕的：全局解释锁阻止了它们真实地执行并行计算，并且抢占式切换让它们容易发生竞争。异步通常是正确的选择。但是随着基于回调的异步代码增长，它往往会变成一团糟。协程是一个不错的选择。它们自然地将异常处理和堆栈跟踪纳入子程序。

如果我们眯着眼并模糊的看`yield from`语句，协程看起来就像传统的阻塞`I/O`线程。甚至我们可以用多线程编程中的经典模式来协调协程。无需重复造轮子。因此，与回调相比，协程对于多线程编程经验丰富的程序员来说是一种更有吸引力的习惯用法。

但是当我们睁开眼并聚焦到`yield from`语句时，我们可以看到，当协程放弃控制权并允许其他代码运行时，它们会标记一个点。不同于线程，协程展示了我们的代码在哪里可以被打断哪里不能被打断。`Glyph Lefkowitz`在他富有启发性的文章《Unyielding》中写道，“线程使局部推理变得困难，局部推理也许是软件开发中最重要的事情。”然而，显示的`yilding`使"通过检查例程本身而不是检查整个系统来理解例程的行为（原因与正确性）"变得可能。

本章是在`Python`和异步技术的复兴中撰写的。基于生成器的协程(你刚刚了解了它的设计)，在`Python3.4`的`asyncio`模块中，于`2014年3月发布`。在`2015年的9月`，`Python 3.5`发布了语言本身内置的协程。这些原生的协程使用新的语法`"async def"`声明，并替代了`"yield from"`，它们使用了心得`"await"`关键词来委托以协程或者等待`Future`。

尽管有很多改进，但核心思想仍然没变。`Python`的新的原生的协程在语法上不同于生成器但是工作方式非常相似；实际上，它们在`Python`解释器中共享实现。`Task,Future和事件循环`在`asyncio`将会继续保持规则。

现在你知道了`asyncio`是如何工作的，你很大可能会忘记细节。机械被塞在一个精巧的接口后面。但是你对基本原理的掌握使你能够在现代异步环境中正确而有效地编写代码。



[^1]:  线程相关资源
[^2]: Even calls to `send` can block, if the recipient is slow to acknowledge outstanding messages and the system's buffer of outgoing data is full
[^3]: 原文作者之一
[^4]: http://www.kegel.com/c10k.html[↩](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html#fnref3)
[^ 5]: 原文叫做 `overlapping`I/O,详情请参考：[https://en.wikipedia.org/wiki/Overlapped_I/O](https://en.wikipedia.org/wiki/Overlapped_I/O)
[^6]: Jesse listed indications and contraindications for using async in ["What Is Async, How Does It Work, And When Should I Use It?":](http://pyvideo.org/video/2565/what-is-async-how-does-it-work-and-when-should). Mike Bayer compared the throughput of asyncio and multithreading for different workloads in ["Asynchronous Python and Databases":](http://techspot.zzzeek.org/2015/02/15/asynchronous-python-and-databases/)[↩](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html#fnref5)
[^7]: 这里的中断，就是指假如该程序有 2个协程，那么协程A是不能被协程B关闭\中断（cancel）。（一个协程函数代表一个子协程）而在多线程中，同样我们假设有2个线程，线程A是可以被线程B取消掉（也就是说能在A线程中通过信号取消/中断B线程）

[^8]: For a complex solution to this problem, see http://www.tornadoweb.org/en/stable/stack_context.html[↩](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html#fnref6)
[^9]: The `@asyncio.coroutine` decorator is not magical. In fact, if it decorates a generator function and the `PYTHONASYNCIODEBUG` environment variable is not set, the decorator does practically nothing. It just sets an attribute, `_is_coroutine`, for the convenience of other parts of the framework. It is possible to use asyncio with bare generators not decorated with `@asyncio.coroutine` at all.[↩](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html#fnref7)
[^ 10]:  Python 3.5's built-in coroutines are described in [PEP 492](https://www.python.org/dev/peps/pep-0492/), "Coroutines with async and await syntax."[↩](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html#fnref8) 

[^ 11]: This future has many deficiencies. For example, once this future is resolved, a coroutine that yields it should resume immediately instead of pausing, but with our code it does not. See asyncio's Future class for a complete implementation.[↩](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html#fnref9)

[^12]: In fact, this is exactly how "yield from" works in CPython. A function increments its instruction pointer before executing each statement. But after the outer generator executes "yield from", it subtracts 1 from its instruction pointer to keep itself pinned at the "yield from" statement. Then it yields to *its* caller. The cycle repeats until the inner generator throws `StopIteration`, at which point the outer generator finally allows itself to advance to the next instruction.[↩](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html#fnref10)
[^ 13]:https://docs.python.org/3/library/queue.html[↩](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html#fnref11)

[^ 14]:The actual `asyncio.Queue` implementation uses an `asyncio.Event` in place of the Future shown here. The difference is an Event can be reset, whereas a Future cannot transition from resolved back to pending.[↩](#fnref14)