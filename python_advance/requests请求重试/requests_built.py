import requests
from requests.adapters import HTTPAdapter

from normal import BaseDictData


def get_data(url: str, max_retry: int = 0, time_out: float = 1., **kwargs) -> BaseDictData:
    """
    自动重试 timeout 错误 的方法, 用 requests 自带轮子完成！
    :param url: 请求的 url
    :param max_retry: 最大重试次数
    :param time_out: 超时重试时间
    :param kwargs: 可选命名参数
    :return: BaseDictData
    """
    session: requests.Session = kwargs.get("session", requests.Session())  # 获取session 或者新建 session
    params: BaseDictData = kwargs.get("params", {})  # 不管你传了什么奇怪的东西， 我只收这个
    headers: BaseDictData = kwargs.get("headers", {})  # 同上
    adapter: HTTPAdapter = HTTPAdapter(max_retries=max_retry)  # 初始自带处理额外操作的适配器
    session.mount("http://127.0.0.1", adapter=adapter)  # 给我们的 session 安装上 adapter, 第一个参数为主机，代表对于哪台主机的请求需要装上适配器
    try:
        response: requests.Response = session.get(
            url,
            params=params,
            headers=headers,
            timeout=time_out
        )
    except requests.ConnectionError:
        print(f"{max_retry + 1}次请求都失败了，即将返回空值，请耐心等待...")
    else:
        session.close()  # 关闭 session, 源码主要是清除所有装配器
        return response.json()
    return {}


if __name__ == '__main__':
    res = get_data("http://127.0.0.1:5000/api/retry", 1)
    print(res)
