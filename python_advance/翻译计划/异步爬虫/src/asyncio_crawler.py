try:
    from asyncio import JoinableQueue as Queue, CancelledError
except ImportError:
    # 在 Python 3.5，asyncio.JoinableQueue 并入到了 Queue
    from asyncio import Queue, CancelledError
import asyncio

import aiohttp

loop = asyncio.get_event_loop()


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

    @asyncio.coroutine
    def crawl(self):
        """运行 crawler 直到所有的工作完成"""
        wokers = [asyncio.Task(self.work())
                  for _ in range(self.max_tasks)]

        # 当所有任务完成，退出
        yield from self.q.join()
        for w in wokers:
            w.cancel()

    @asyncio.coroutine
    def work(self):
        while True:
            url, max_redirect = yield from self.q.get()

            # 下载页面并向 self.q 中增加新链接
            yield from self.fetch(url, max_redirect)
            self.q.task_done()

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


class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

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

    def cancel(self):
        self.coro.throw(CancelledError)

    def __str__(self):
        return self.__class__.__name__


crawler = crawling.Crawler('http://xkcd.com',
                           max_redirect=10)

loop.run_until_complete(crawler.crawl())
