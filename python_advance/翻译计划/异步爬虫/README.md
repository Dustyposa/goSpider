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

