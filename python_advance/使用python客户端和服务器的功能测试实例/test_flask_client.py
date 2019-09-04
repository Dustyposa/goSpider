import json
import typing
import unittest

from flask_basic import app as my_app


class TestApp(unittest.TestCase):

    def setUp(self) -> None:
        self.client = my_app.test_client()  # 初始化客户端，app 自带的测试客户端

    def test_msg_api(self) -> None:
        response = self.client.get("/api")  # 访问路由
        data: typing.Dict[str, typing.Any] = json.loads(response.data.decode("u8"))  # 响应数据格式化
        self.assertEqual(data["Hello"], "World!")  # 判断结果

    def test_goods_api(self) -> None:
        response = self.client.get("/goods/123")  # 访问路由
        data: typing.Dict[str, typing.Any] = json.loads(response.data.decode("u8"))  # 响应数据格式化
        self.assertEqual(data["name"], "cake")  # 判断结果
        self.assertEqual(data["id"], 123)  # 判断结果

    def test_404_page(self) -> None:
        response = self.client.get("/idontknow")  # 访问路由
        self.assertEqual(response.status, "404 NOT FOUND")  # 404 状态监测
        data: typing.Dict[str, typing.Any] = json.loads(response.data.decode("u8"))  # 响应数据格式化
        self.assertEqual(data["msg"], "no route")  # 返回数据监测


if __name__ == '__main__':
    unittest.main()
