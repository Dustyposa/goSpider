from typing import Dict, Any

import requests

BaseDictData = Dict[str, Any]


def get_data(url: str, max_retry: int = 0, time_out: float = 3., **kwargs) -> BaseDictData:
    """自动重试 timeout 错误 的方法"""
    params: BaseDictData = kwargs.get("params", {})  # 不管你传了什么奇怪的东西， 我只收这个
    headers: BaseDictData = kwargs.get("headers", {})  # 同上
    for i in range(max_retry + 1):
        """进行最大重试次数的遍历"""
        try:
            response: requests.Response = requests.get(
                url=url,
                params=params,
                headers=headers,
                timeout=time_out,
            )
        except requests.ReadTimeout:
            print(f"第{i + 1}次请求失败，正在重试。")
        else:
            return response.json()  # 没有错误，直接返回

    print(f"{max_retry + 1} 次请求都失败了，返回空值，便于后续逻辑处理。。。")
    return {}


if __name__ == '__main__':
    print(get_data("http://localhost:5000/api/retry", max_retry=1, time_out=.01))
