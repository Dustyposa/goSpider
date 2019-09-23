import wrapt
from functools import wraps
from typing import Tuple

import requests

from normal import BaseDictData


def strong_retry(
        max_retry: int = 3,
        exception: Tuple[BaseException] = (
                requests.ConnectTimeout,
                requests.ReadTimeout,
        )
):
    """
    万能函数重试装饰器诞生！
    :param max_retry: 最大重试次数
    :param exception: 捕捉错误类型
    :return:
    """

    def retry(func):
        @wraps(func)  # 保留被装饰函数的元信息
        def closure(*args, **kwargs) -> BaseDictData:
            for i in range(max_retry + 1):
                try:
                    res = func(*args, **kwargs)
                except exception:
                    print(f"第{i + 1}次重试。")
                else:
                    return res
            return {}

        return closure

    return retry


def strong_common_retry(
        max_retry: int = 3,
        exception: Tuple[BaseException] = (
                requests.ConnectTimeout,
                requests.ReadTimeout
        )
):
    """
    万能重试装饰器诞生！
    :param max_retry: 最大重试次数
    :param exception: 捕捉错误类型
    :return:
    """

    @wrapt.decorator  # 保留被装饰函数的元信息
    def wrapper(wrapped, instance, args, kwargs) -> BaseDictData:
        """

        :param wrapped:
        :param instance:如果被装饰者为普通类方法，该值为类实例
                        如果被装饰者为 classmethod 类方法，该值为类
                        如果被装饰者为类/函数/静态方法，该值为 None
        :param args:
        :param kwargs:
        :return:
        """
        for i in range(max_retry + 1):
            try:
                res = wrapped(*args, **kwargs)
            except exception:
                print(f"第{i + 1}次重试。")
            else:
                return res
        return {}

    return wrapper


@strong_common_retry()
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


if __name__ == '__main__':
    r = get_data("http://127.0.0.1:5000/api/retry", time_out=1.)
    print(r)
