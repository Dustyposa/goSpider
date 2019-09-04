import typing
from urllib import parse

import requests


MyResponse = typing.Dict[str, typing.List[str]]


class MySpider:
    """拼接返回的id"""
    def __init__(self, url="http://example.com") -> None:
        self.url: str = url
        self.return_base_url: str = "http://shop.com/id/"

    def get_data(self):
        try:
            response: requests.Response = requests.get(self.url)
        except requests.exceptions.ConnectionError:
            # 链接超时
            return self._handle_data()
        else:
            response.raise_for_status()  # 检查请求状态值200
        data = response.json()
        return self._handle_data(data)

    def _handle_data(self, data=None) -> MyResponse:
        """处理请求的数据"""
        if data:
            return_data: typing.List[str] = []
            all_id = data.get("all_id", [])
            for goods_id in all_id:
                return_data.append(parse.urljoin(self.return_base_url, goods_id))
            return {"data": return_data}
        return {"data": []}
