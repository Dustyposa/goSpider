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


class EventLoop:
    def run_until_complete(self, coro):
        """运行直到生成器结束"""
        task = Task(coro)
        task.task_done_callback(stop_callback)
        try:
            self.run_forever()
        except StopError:
            pass


class StopError(BaseException):
    """抛出停止事件循环"""


def stop_callback(future):
    raise StopError

