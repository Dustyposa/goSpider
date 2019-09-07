import unittest
from unittest import mock

import requests
import requests_mock

from client import MySpider, MyResponse


class TestMySpider(unittest.TestCase):
    def setUp(self) -> None:
        self.spider: MySpider = MySpider()  # 初始化对象，首先运行这里，再运行 test_xxxxxx

    def test_handle_data(self) -> None:
        """测试处理代码的逻辑"""
        return_data: MyResponse = {"data": []}  # 返回的基础数据
        self.assertEqual(self.spider._handle_data(), return_data)  # none值返回，测试是否相等

        return_data.update(data=[
            "http://shop.com/id/23",
            "http://shop.com/id/32"
        ])  # 生成正常值
        # 正常值返回, 测试是否相等
        self.assertEqual(self.spider._handle_data({"all_id": ["23", "32"]}), return_data)

    @requests_mock.mock()
    def test_get_data(self, mocker) -> None:
        """测试正常逻辑"""
        shop_data: MyResponse = {"all_id": ["12", "123", "1234"]}
        mocker.get(requests_mock.ANY, json=shop_data)  # 截胡 requests.get

        spider_data: MyResponse = self.spider.get_data()  # 获取正常返回值
        response_data: MyResponse = {'data': ['http://shop.com/id/12', 'http://shop.com/id/123', 'http://shop.com/id/1234']}
        self.assertEqual(spider_data, response_data)  # 比较是否相等

        shop_data: MyResponse = {}
        mocker.get(requests_mock.ANY, json=shop_data)  # 截胡 requests.get
        spider_data: MyResponse = self.spider.get_data()  # 获取空返回值
        response_data: MyResponse = {'data': []}
        self.assertEqual(spider_data, response_data)  # 比较是否相等

    @mock.patch.object(requests, "get", side_effect=requests.ConnectionError("No network"))
    def test_net_error(self, mocked) -> None:
        return_data: MyResponse = {"data": []}
        spider_data: MyResponse = self.spider.get_data()  # 获取网络错误的返回值
        self.assertEqual(spider_data, return_data)


if __name__ == '__main__':
    unittest.main()
