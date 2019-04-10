 requests 强大的请求工具 
---
### 基本使用
#### 请求参数
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
#### 请求方式
##### 1. Get 请求
##### 2. Post 请求
##### 3. 其他请求
> 参考资料
>> [requests官方中文文档](http://docs.python-requests.org/zh_CN/latest/) 
