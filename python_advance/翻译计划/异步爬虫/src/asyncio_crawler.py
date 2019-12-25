try:
    from asyncio import JoinableQueue as Queue
except ImportError:
    # 在 Python 3.5，asyncio.JoinableQueue 并入到了 Queue
    from asyncio import Queue
import asyncio

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


crawler = crawling.Crawler('http://xkcd.com',
                           max_redirect=10)

loop.run_until_complete(crawler.crawl())
