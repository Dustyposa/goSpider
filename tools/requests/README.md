 requests 强大的请求工具 
 - [请求](https://github.com/Dustyposa/goSpider/tree/master/tools/requests#请求)
    + [请求头通用参数](https://github.com/Dustyposa/goSpider/tree/master/tools/requests#通用请求参数)
    + [Get请求](https://github.com/Dustyposa/goSpider/tree/master/tools/requests#1.Get请求)
    + [Post请求](https://github.com/Dustyposa/goSpider/tree/master/tools/requests#2.Post请求)
    + [其他请求](https://github.com/Dustyposa/goSpider/tree/master/tools/requests#3.其他请求(作用Restful接口))
 - [响应](https://github.com/Dustyposa/goSpider/tree/master/tools/requests#响应)
    + [状态码](https://github.com/Dustyposa/goSpider/tree/master/tools/requests#状态码)
    + [文本内容](https://github.com/Dustyposa/goSpider/tree/master/tools/requests#文本内容)
    + [json对象](https://github.com/Dustyposa/goSpider/tree/master/tools/requests#json对象)
    + [二进制内容](https://github.com/Dustyposa/goSpider/tree/master/tools/requests#二进制内容)
 
---
## 请求
### 基本使用
#### 通用请求参数
**url**  
你的请求地址
```
>>> url = "https://api.github.com/use"
>>> response = requests.get(url=url)
```
**params**  
URL 参数  
url 参数是指 在url中传递的参数 形式例如：
> 单个参数 键为 key 值为 value  
> https://api.github.com/use?key=value 
```
>>> params = {"key": "value"}
>>> response = requests.get(url=url, params=params)
>>> response.url  # 请求地址
'https://api.github.com/use?key=value'
```
> 多个参数 键1为 key1 值为 value1 键2为 key2 值为 value2  
> https://api.github.com/use?key1=value1&key2=value2  
```
>>> params = {"key1": "value1", "key2": "value2"}
>>> response = requests.get(url=url, params=params)
>>> response.url  # 请求地址
'https://api.github.com/use?key1=value1&key2=value2'
```
> 重复key传递 key1 有两个值 value1, value2  
> https://api.github.com/use?key1=value1&key1=value2 
```
>>> params = {"key1": ["value1", "value2"]}
>>> response = requests.get(url=url, params=params)
>>> response.url  # 请求地址
'https://api.github.com/use?key1=value1&key1=value2'
```
**headers**  
请求头  
是指该请求发送时的请求报文  
```
>>> headers = {"name": "gakki"}
>>> response = requests.get(url=url, headers=headers)
>>> response.request.headers
{'User-Agent': 'python-requests/2.19.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'name': 'gakki'}
```
修改User-Agent 不区分大小写的哦  
> HTTP报头的名称是不区分大小写，根据[RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)
```
>> headers = {"user-agent": "it's me"}
>> response = requests.get(url=url, headers=headers)
>> response.request.headers
{'User-Agent': 'python-requests/2.19.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'name': 'gakki'}
```
**cookie**  
就是记录请求者是谁的啦！  
当然cookie也可以写到 headers中
> headers = {"cookie": "xxx"}
```
>>> cookie = {"who are you": "cookie"} 
>>> response = requests.get(url=url, cookies=cookie)
>>> response.request.headers
{'User-Agent': 'python-requests/2.19.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Cookie': 'who are you=cookie'}
```
**timeout**
> 设置请求等待时长，避免长阻塞 单位:秒(s)
```
>>> requests.get(url=url, timeout=0.01)
...
... 超时错误
ConnectTimeout: HTTPSConnectionPool(host='api.github.com', port=443): Max retries exceeded with url: /use (Caused by ConnectTimeoutError(<urllib3.connection.VerifiedHTTPSConnection object at 0x0000000006408438>, 'Connection to api.github.com timed out. (connect timeout=0.01)'))
```
> 未超时

`requests.get(url=url, timeout=3)`
#### 请求方式
##### 1. Get 请求
```
>>> response = requests.get('https://api.github.com/events')
>>> 
>>> # 传递参数
>>> params = {"key": "value"}
>>> response = requests.get('https://api.github.com/events', params=params)
```
##### 2. Post 请求
传递post参数  **data**  
> 表单请求
```
>>> data = {"key": "value"}  
>>> response = requests.post(url="http://httpbin.org/post", data=data)  # 当data是dict对象时，该请求以form-data的形式传递
>>> response.json()
{
  ...
  "form": {
    "key": 
      "value"
  },
  ...
}
```
> 表单多个元素使用同一key时，利用元组传递请求的form-data
```
>>> data = (('key1', 'value1'), ('key1', 'value2'))
>>> response = requests.post('http://httpbin.org/post', data=data)
>>> response.json()
{
  ...
  "form": {
    "key1": [
      "value1",
      "value2"
    ]
  },
  ...
}
```
**json**参数  
> 传递非表单数据(非dict类型),string类型

```
>>> json_data = {"key": "value"}
>>> response = requests.post('http://httpbin.org/post', json=json_data)
>>> response.json()
{
    ...
    'data': '{"key": "value"}',
    'files': {},
    'form': {},
    ...
}
```
**files**参数  
> 传递多部分编码(Multipart-Encoded)的文件
```
>>> url = 'http://httpbin.org/post'
>>> files = {'file': open('report.xls', 'rb')}  # 以二进制方式打开，只需要文件描述符
>>> response = requests.post(url, files=files)
>>> response.text
{
  ...
  "files": {
    "file": "<censored...binary...data>"
  },
  ...
}
```

##### 3. 其他请求(作用 Restful 接口) 
```
>>> response = requests.put('http://httpbin.org/put', data = {'key':'value'})  # put 请求
>>> response = requests.delete('http://httpbin.org/delete')  # delete 
>>> response = requests.head('http://httpbin.org/get')  # head
>>> response = requests.options('http://httpbin.org/get')  # options
```
## 响应
#### 状态码
##### **status_code** 响应状态码
```
>>> response = requests.get('http://httpbin.org/get')
>>> response.status_code
200
>>> response.status_code == requests.codes.ok  # 内置查询对象
True
```
#### 文本内容
##### **text** 响应文本内容(根据报文，已经转码)
```
>>> response = requests.get('http://httpbin.org/get')
>>> response.text

'{\n  "args": {}, \n  "headers": {\n    "Accept": "*/*", \n  ...... \n  "url": "https://httpbin.org/get"\n}\n'
```
#### json对象
##### **json()** 获取响应的json对象
```
>>> response = requests.get('http://httpbin.org/get')
>>> response.json()
{   
    'args': {},
    ...
    'url': 'https://httpbin.org/get'
    }
```
#### 二进制内容
##### **content** 获取二进制内容
```
>>> response = requests.get('http://httpbin.org/get')
>>> response.content
b'{\n  "args": {},...... "url": "https://httpbin.org/get"\n}\n'
```






> 参考资料
>> [requests官方中文文档](http://docs.python-requests.org/zh_CN/latest/) 
