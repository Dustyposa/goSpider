
# segmentfault 社区异步抓取
https://segmentfault.com/

本项目主要是ajax分析练习抓取练习.话不多说，开始我们的抓取之旅吧！
### 1. [首页分析](#1-首页分析)  # 需要的数据请求地址分析

#### [完整代码 jupyter_notebook](./example.ipynb)

### 1. 首页分析。
   - #### 打开 [目标url](https://segmentfault.com/), 定位数据位置
      ![爬取源网址](./images/s_index.png)  
   - #### 进行数据定位。  
      ![数据搜索](./images/1_s.png)  
      由图可得，我们第一页的数据应该是没问题的。但是第二页在哪里？我们往下看看。
### 2. ajax页面分析
   - #### 寻找下一页
      我们进行鼠标滚动操作，继续往下找。我们虽然不断的再滚动滚轮，但是数据却没有到达底部，还在源源不断的出来。那么很明显，这里有ajax请求！
      因为在首页的抓取中，我们根本没有发现这些数据。
      ![ajax页面](./images/ajax.gif)  
   - #### 确认数据请求来源
        好东西，居然突然出现，那我们来抓包看看这些数据到底哪里来的？  
        PS：这里有个小技巧，我们可以只看ajax请求
        ![only_ajax](./images/skill.png)  
        查看所有ajax请求（因为这里请求很少，我们就不用搜索了，直接查看即可）：
        ![ajax抓包](./images/ajax_data.png)  
      上图可知，这个recommend接口就是能产生源源不断的数据！并且数据格式是json，那么处理也就更简单了！ 
   - #### 查看headers，分析请求报文
      ![请求分析](./images/request_ana.png)  
      我们看到该接口，有两个参数，`page`，和`_`,这个`page`肯定是控制推荐页数的，在第一页请求时没有携带，肯定对方服务器做了处理，第一页我们同样传`page=1`即可。后面这个`_`参数根据推荐系统来说，应该是个群体代号或者用户id，但是我并没有登录，那么目前传递的这个参数很可能是个通用的id。  
      分析结果如图，所以我们可以得出以下结论：  
        首页接口:

        | 信息     | 结果                                  |
        | :------- | -------------------------------------|
        | 请求地址 | <https://segmentfault.com/> |
        | 请求方法 | Get                                   |
        | 响应格式 | text 文本                             |
        | 编码     | UTF-8                                |
        | 参数     |None                        |


   推荐信息接口:  

   | 信息     | 结果                                  |
   | :------- | -------------------------------------|
   | 请求地址 | <https://segmentfault.com/api/timelines/recommend> |
   | 请求方法 | Get                                   |
   | 响应格式 | json                            |
   | 编码     | UTF-8                                |
   | 参数     |page, _                        |

## 2. 利用requests进行数据抓取
分析已经完成，那么写代码。当然是分分钟的事情啦！  
话不多说，直接开撸。


模块导入
```python
>>> import requests
>>> from requests.exceptions import HTTPError
```
#### 获取首页数据
    定义首页获取函数 `get_data`：
    ```python
    def get_data(url):
    
        response = requests.get(url)
        if response.status_code == requests.codes.ok:  # 检测状态码
            return response.text  # 返回响应的文本信息
        else:
            response.raise_for_status()  # 4xx 5xx 时,引出错误 代替 raise requests.exception.HTTPError
    
    url = "https://segmentfault.com"
    data = get_data(url)  # 获取数据
    data_res = {}  # 存储数据的初始化字典
    data # 查看数据
    ```
    ```
    \n<!DOCTYPE HTML><html lang="zh-CN"><head><meta charset="UTF-8"/><meta http-equiv="X-UA-Compatible" content="IE=edge, chrome=1"/><meta name="renderer" content="webkit"/><meta property="qc:admins" content="15317273575564615446375"/><meta property="og:image" content="https://static.segmentfault.com/v-5c8b4d77/global/img/t
    ......
    ```

####  Scrapy 提取首页数据 
   - scrapy 混合提取，个人习惯，选用该提取方式
    
    ```python
    >>> from scrapy import Selector  # 导入scrapy的选择器
    ```
    ```python
    se = Selector(text=data)
    ```
    
    
    
    ```python
    >>> se = Selector(text=data)
    ```
    
    #### 提取规则说明 从下方案例可以看出,scrapy的提取器,css和xpath,以及正则提取都是支持的,我们可以混用  
       - .css()  # 就是css规则的提取
       - .xpath()  # 就是xpath规则的提取,需要注意的是,因为scrapy的Selector支持混用,如果xpath是在某个提取器之后,那么必须使用"./"来跟进上个提取器的提取点,不能使用"//", 因为Selector 的xapth提取器的"//"永远代表根节点
           - response.css("#id").xpath("./a")  # 该规则表示id="id" 的节点**之后**的所有a标签节点
           - response.css("#id").xpath("//a")  # 改规则就变成了提取所有的a标签节点,前面的css选择器的结果失效.
       - .re()  # 就是正则的提取, 正则提取后,不需要用extract()来转化成str类型
       - extract()  # 将当前的选择结果转化成str类型  
    
    
    ```python
    >>> poster = se.css(".nbg img").xpath("./@src").extract()  # 获取海报
    >>> movie_name = se.css("div.pl2").xpath("./a/text()").re("\w+")  # 获取电影名
    >>> other_name = se.css("div.pl2").xpath("./a/span/text()").extract()  # 获取电影别名
    >>> time_actor = se.css("div.pl2").xpath("./p/text()").extract()  # 获取上映日期和演员
    >>> score = se.css("span.rating_nums::text").extract()  # 获取评分
    >>> comment_people = se.xpath('//span[@class="pl"]/text()').extract()  # 获取评分人数
    >>> movie_data = {}
    ```
    
    
    ```python
    for p, m, o, t, s, c in zip(poster, movie_name, other_name, time_actor, score, comment_people):
        release_time, actor = get_time_actor(t)
        movie_data.update({m: {"poster": p, "movie_name": m, "other_name": t, "release_time": release_time, "actor": actor, "score": s, "comment": c}})
    print(movie_data)
    ```
    ```
        {
        '辛德勒的名单': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p492406163.jpg', 'movie_name': '辛德勒的名单', 'other_name': '1993-11-30(华盛顿首映) / 1994-02-04(美国) / 连姆·尼森 / 本·金斯利 / 拉尔夫·费因斯 / 卡罗琳·古多尔 / 乔纳森·萨加尔 / 艾伯丝·戴维兹 / 马尔戈萨·格贝尔 / 马克·伊瓦涅 / 碧翠斯·马科拉 / 安德烈·瑟韦林 / 弗里德里希·冯·图恩 / 克齐斯茨托夫·拉夫特...', 'release_time': ['1993-11-30(华盛顿首映)', '1994-02-04(美国)'], 'actor': ['连姆·尼森', '本·金斯利', '拉尔夫·费因斯',
        ......
        }
    ```

## 总结
以上就是我们该次提取练习的所有内容,以豆瓣电影top100的响应为例,我们讲解了常用的5种提取器.  
**1. 正则**  
   - "." 表示任意非空格换行等字符
   - ".*?"  表示贪婪匹配,最少匹配一次
   - "()"  表示提取()中的内容
   -  "\\w" 表示正常字符,比如英文字母,中文等常见文字
   - ".+"  表示至少匹配一次任意字符  

**2. css**  
- "." 表示class 
- " "表示子孙节点  
- img 就是img节点  
- a 就是a节点
- "#abd" 表示 id="abc"的节点


#### [完整代码](./douban_spider.ipynb)
