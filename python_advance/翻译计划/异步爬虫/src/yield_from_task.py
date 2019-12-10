import socket
from typing import Callable
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()  # 创建选择器对象


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


class Fetcher:
    def __init__(self, url: str) -> None:
        self.response = b""
        self.url = url
        self.sock = None

    def fetch(self) -> None:
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('httpbin.org', 80))
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
        print('connected')
        selector.unregister(self.sock.fileno())
        print('send data')
        request = f'GET {self.url} HTTP/1.1\r\nHost: httpbin.org\r\n\r\n'  # 构建请求头
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
            print('chunk:', chunk)
            selector.unregister(self.sock.fileno())
            if chunk:
                print('data get')
                self.response += chunk
            else:
                # 响应读取完成
                break
        print('response:', self.response)


stoped = False


def loop() -> None:
    while not stoped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()


if __name__ == '__main__':
    # 开始抓取 http://xkcd.com/353
    fetcher = Fetcher('/get')
    Task(fetcher.fetch())

    loop()
