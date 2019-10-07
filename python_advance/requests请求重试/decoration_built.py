import functools
import time
import types
from typing import Callable

import requests
from requests.adapters import HTTPAdapter

from normal import BaseDictData


class RequestsRetry:
    def __init__(self, max_retry: int, func: Callable) -> None:
        """需要注意。被装饰的函数是最后传入的。"""
        self.max_retry = max_retry
        functools.wraps(func)(self)  # 保留原函数的元信息
        self.func = func

    def __call__(self, *args, **kwargs) -> BaseDictData:
        """装饰器处理逻辑函数"""
        session: requests.Session = kwargs.get("session", requests.Session())  # 获取session 或者新建 session
        max_retry: requests.Session = kwargs.get("max_retry")  # 获取 max_retry
        adapter: HTTPAdapter = HTTPAdapter(max_retries=max_retry)  # 初始自带处理额外操作的适配器
        session.mount("http://", adapter=adapter)  # 给我们的 session 安装上 adapter, 第一个参数为前缀，代表哪种请求需要装上适配器
        kwargs.update(session=session)  # 更新 session， 如果没有传session，就将带适配器的 session 传入命名参数
        try:
            response: BaseDictData = self.func(*args, **kwargs)
        except requests.ConnectTimeout:
            print(f"{max_retry}次请求都超时了，即将返回空值，请耐心等待返回空值")
            return {}
        else:
            return response

    def __get__(self, instance, owner) -> object:
        """实现该方法后，可以将装饰器器用于类的函数的装饰。"""
        if instance is None:
            return self
        return types.MethodType(self, instance)  # 如果有参数，就绑定至self

    def itself(self, *args, **kwargs) -> BaseDictData:
        """不做处理，调用本身"""
        return self.func(*args, **kwargs)


def retry(max_retry: int = 3):
    """装饰器包装，增加请求重试参数。"""
    # 此处为了避免定义额外函数，直接使用 functools.partial 帮助构造 RequestsRetry 实例
    return functools.partial(RequestsRetry, max_retry)


@retry()
def get_data(url: str, time_out: float = 3., **kwargs) -> BaseDictData:
    """
    自动重试 timeout 错误 的方法, 用 requests 自带轮子完成！
    :param url: 请求的 url
    :param time_out: 超时重试时间
    :param kwargs: 可选命名参数
    :return: BaseDictData
    """
    session: requests.Session = kwargs.get("session", requests.Session())  # 获取session 或者新建 session
    params: BaseDictData = kwargs.get("params", {})  # 不管你传了什么奇怪的东西， 我只收这个
    headers: BaseDictData = kwargs.get("headers", {})  # 同上
    with session.get(url, params=params, headers=headers, timeout=time_out) as response:
        return response.json()


class MySpider:
    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("reset for one second")
        time.sleep(1)
        res_data = self.func(*args, **kwargs)
        return res_data

    def at_once_run(self, *args, **kwargs):
        print("now, run the function")
        return self.func(*args, **kwargs)


@MySpider
def spider():
    print("正在抓取")


if __name__ == '__main__':
    # res = get_data("http://127.0.0.1:5000/api/retry", time_out=1.)
    # print(res)
    # spider = MySpider(spider).at_once_run
    # spider = MySpider(spider)

    spider.at_once_run()
