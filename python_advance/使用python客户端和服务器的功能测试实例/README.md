
>### 编写功能测试的目的
>验证应用的行为和期望一致的测试
确认异常修复的测试（增加测试覆盖率）
想想一个场景，因为接口需要增加一些功能，而更改了一些代码。
那么修改的代码会不会对之前的功能有影响呢？测试就来了。
**并且，良好的编写测试习惯，持续地写测试写文档写代码是必备的。更改代码也更加方便（重构），只用相同的测试代码即可。而且还能提升代码的可读性，测试代码也是功能的描述。**
#### 测试的分类
1. 单元测试（unit test）# 主要测函数
2. 功能测试（function test）# 主要测某些代码段完整的功能
3. 集成测试（integration test）  # 主要在线上环境测试
4. 负载/压力测试 （load test）  # 大家比较熟悉
5. 端到端测试 （end-to-end test） # 完整的测试产品

本文主要讲解功能测试实例的编写。


在python中编写功能测试代码
---
主要分为两部分，客户端测试和服务器端测试。
目的都是为了检测自己写的代码是否实现了自己想要的功能。
> 功能测试组要注意的点：
> **功能测试都不占用网络服务资源，请求都直接模拟网络资源**
>
**客户端测试可以用在哪里呢？**
> 带有请求的地方都可以:
> **爬虫**
> **调用第三方的接口**（OSS， 数据库， AI服务等）

PS: 为了提升代码质量，所有代码都会使用静态注释,你的`python version` 需要 >= 3.5
**如何实现网络资源请求的模拟呢？这时候，我们的 mock 就要出场了。**
### 1. 客户端测试 request_mock
首先，我们编写一个简单的客户端，当作我们用来测试的客户端 `client.py`，代码如下:
```python
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

```

客户端简单的实现了一个请求网站并处理返回数据的逻辑.
那么，开始测试我们的客户端吧！
记住：**这是功能测试，与网络资源访问无关，我们只需要测试功能逻辑！其余第三方对象用模拟对象即可！**
一般的对象，`unittest` 自带的 `mock` 对象就能满足。那么如何网络模拟对象的实现呢？这时候，我们的 `requests_mock` 就要登场了。
它会实现对请求的拦截，以此达到我们想要的效果。
测试代码 `test_client.py` 如下:
```python
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
```
我们运行一下就能看到测试的结果。
整个测试代码整体也比较简单，
`requests_mock` 作为一个装饰器，`reqeusts`进行了拦截。之后就直接进行了设定值的返回。
需要注意的几个函数:
1. `unittest` 为 python 标准库，可以直接导入并使用，不过后续的文章我们会升级成 `pytest` , 可定制性更强。
2. 安装 `requests_mock` , 也比较简单，直接 `pip install reqeusts_mock` 即可，后续我们会进行 `requests_mock` 的源码分析。并且，`reqeusts_mock` 的源码对于学习静态注释也是极好的。
3. `@unittest.mock.patch.object` 是进行对象层面的异常状态抛出，当 `requests` 对象调用 `get` 方法时，便抛出错误。
### 2. 测试服务器端
其实客户端的测试比服务器端难一些。
> 因为服务器端的测试，框架已经帮你封装好了！
> **服务端功能测试用在哪？当然是测自己写的接口啦！**

测试步骤类似，编写服务器，我们用 `flask` 和 `starlette` 进行举例，分别代表`python` 同步web框架和异步web框架。
#### flask
我们编写一个简单的`flask_server.py`, 代码如下:
```python
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api', methods=["GET"])
def msg_api():
    """常规返回"""
    return jsonify({'Hello': 'World!'})


@app.route('/goods/<int:goods_id>', methods=["GET"])
def query_goods(goods_id):
    """带id的路由"""
    return jsonify({"name": "cake", "id": goods_id})


@app.errorhandler(404)
def error_404_handing(error):
    """404页面"""
    return jsonify({"msg": "no route", "err": str(error)}), 404


if __name__ == '__main__':
    app.run()

```
代表也比较简单，有3个路由
1. 常规返回的路由 `/api`
2. 路由带id `/goods/123123`
3. 404 页面 
测试代码`test_flask_client.py` 代码如下:
```python
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
```
整个代码也就很简单清晰了，因为`flask` 自带的`app`就包含了测试客户端，只需要请求检查响应即可，整个过程可以一气呵成！
#### starletee
我们编写 `starletee` 的服务器文件 `starletee_server.py`,代码如下:
```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()


@app.route('/api', methods=["GET"])
async def hello_api(request) -> JSONResponse:
    """常规返回"""
    return JSONResponse({'Hello': 'World!'})


@app.route('/goods/{goods_id:int}', methods=["GET"])
async def query_goods(request) -> JSONResponse:
    """带id的路由"""
    return JSONResponse({"name": "cake", "id": request.path_params.get("goods_id")})


@app.exception_handler(404)
async def not_found(request, exc) -> JSONResponse:
    """404处理"""
    return JSONResponse(content={"msg": "no route"}, status_code=exc.status_code)
```
`starletee`整体代码和`flask`很相似，所以遇到新的框架不要畏惧，大体其实是差不多的，只有一些小细节不一样，例如：
1. `flask` 的 `request`对象是全局的，而 `starletee`的 `request`对象和`django`的 `request`对象相似，都是在分发在路由中。
2. 路由中的变量获取方式不同，一个存在参数中，一个存在请求对象中。
3. 错误状态码处理方式返回数据格式不同。

下面为测试`starletee`的代码`test_starletee_api.py`:
```python
import typing
import unittest

from starlette.testclient import TestClient

from starletee_server import app as my_app


class TestApp(unittest.TestCase):

    def setUp(self) -> None:
        self.client = TestClient(my_app)  # 初始化客户端，app 自带的测试客户端

    def test_msg_api(self) -> None:
        response = self.client.get("/api")  # 访问路由
        data: typing.Dict[str, typing.Any] = response.json()  # 响应数据格式化
        self.assertEqual(data["Hello"], "World!")  # 判断结果

    def test_goods_api(self) -> None:
        response = self.client.get("/goods/123")  # 访问路由
        data: typing.Dict[str, typing.Any] = response.json()  # 响应数据格式化
        self.assertEqual(data["name"], "cake")  # 判断结果
        self.assertEqual(data["id"], 123)  # 判断结果

    def test_404_page(self) -> None:
        response = self.client.get("/idontknow")  # 访问路由
        self.assertEqual(response.status_code, 404)  # 404 状态监测
        data: typing.Dict[str, typing.Any] = response.json()  # 响应数据格式化
        self.assertEqual(data["msg"], "no route")  # 返回数据监测


if __name__ == '__main__':
    unittest.main()
```
除了响应数据的解析方式不同外，其他都一模一样。
对了，有一点不一样，就是客户端的初始化不一样。`TestClient(my_app)`
当然，这只是示例，用的自带的`TestClien`,并且明显比`flask`自带的好用。之后的文章我们会讲解 `WebTest`这个专门设计来作为测试客户端（`flask`中有 `flask_webtest`）
### 3.总结
服务器的功能测试其实很类似，我们可以看到，测试代码几乎不用更改就能使用，那我们思考一下，这样有什么好处呢？
dangdangdang，答案就是：
**在写测试demo时，可以很方便的更换框架来继续进行测试，而不用更改测试代码，所以我们可以选择最适合当前业务的框架来使用！（特别对于微服务来说，针对当前业务，选择最合适的后端。）**

**python客户端和服务器的功能测试流程大题如上文所述，我们需要记住以下几个要点：**
1. 功能测试（及单元测试）不依赖网络资源，IO等，一般使用`MOCK`对象来模拟返回数据。
2. 客户端请求我们可以使用`requests_mock`来模拟，测试自己客户端处理响应的逻辑。
3. 服务器端基本上所有框架都自带有 `test_client` 作为服务器测试客户端（不同框架名字可能不一样，具体参考文档）

[完整代码地址](https://github.com/Dustyposa/goSpider/tree/master/python_advance/%E4%BD%BF%E7%94%A8python%E5%AE%A2%E6%88%B7%E7%AB%AF%E5%92%8C%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%9A%84%E5%8A%9F%E8%83%BD%E6%B5%8B%E8%AF%95%E5%AE%9E%E4%BE%8B)
