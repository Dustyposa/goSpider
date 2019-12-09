def gen_fn():
    result = yield 1
    print(f'result of yield : {result}')
    result2 = yield 2
    print(f'result of 2nd yield : {result2}')
    return 'done'


if __name__ == '__main__':
    gen = gen_fn()
    print(gen.send(None))
    print(gen.send("first yield"))
    print(gen.send("2nd yield"))


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

    import socket

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

