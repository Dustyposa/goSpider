import socket


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

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return

        next_future.add_dpone_callback(future.result)


class Fetcher:
    def __init__(self, url: str) -> None:
        self.response = b""
        self.url = url
        self.sock = None

    def fetch(self) -> None:
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('xkcd.com', 80))
        except BlockingIOError:
            pass
        f = Future()

        def on_connected():
            f.set_result(None)

        selector.register(
            sock.fileno(),
            EVENT_WRITE,
            on_connected
        )
        yield f
        socket.unregister(sock.fileno())
        print('connected')


stoped = False


def loop() -> None:
    while not stoped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()


# 开始抓取 http://xkcd.com/353
fetcher = Fetcher('/353/')
Task(fetcher.fetch())

loop()
