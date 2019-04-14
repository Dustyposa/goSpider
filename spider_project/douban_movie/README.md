
# 豆瓣电影的多方法解析
https://movie.douban.com/tag/Top100  

本项目主要是数据提取的练习,提供了5种数据提取的方式.
### 1. [分析网页]()  # 需要的数据请求地址分析
### 2. [正则提取]()  # 正则提取所须数据
### 3. [Css选择器提取]()  # 利用BeautifulSoup4 进行提取
### 4. [Xpath选择器提取]()  # 利用lxml的etree模块进行xpath提取
### 5. [jQuery提取]()  # 有前端的知识的朋友应该很熟悉,利用的是pyquery模块,节点选择语法与jQuery一致
### 6. [Scrapy 混合提取器]()  # 利用scrapy的Selector模块进行混合提取

### 1. 分析网页，确认爬取目标的数据类型。
   - #### 打开 [目标url](https://movie.douban.com/tag/Top100), 定位数据位置
      ![爬取源网址](./images/index.png)  
   - #### 定位需要的数据位置，查看爬取目标。  
      ![爬取目标](./images/data_target.png)  
      由图可得，我们需要的数据分别为，['海报', '电影名', '上映日期', '演员', '评分', '评价人数']
   - #### 查看请求，分析数据来源请求（F12 >> network 打开请求界面，如下图）
      ![抓包准备](./images/capture_package_ready.png)  
   - #### 确认数据请求来源(Ctrl + F 搜索: 辛德勒)
      ![抓包准备](./images/confirm_request.png)  
      上图可知，该请求只有一个，所以就能轻松的确定来源拉！ 
   - #### 查看headers，分析请求报文
      ![请求分析](./images/requests_ann.png)  
      分析结果如图，所以我们可以得出以下结论：  


| 信息     | 结果                                  |
| :------- | -------------------------------------|
| 请求地址 | <https://movie.douban.com/tag/Top100> |
| 请求方法 | Get                                   |
| 响应格式 | text 文本                             |
| 编码     | UTF-8                                |

## 2. 利用requests进行请求测试
`requests.get`  
定义请求函数，`get_data`  
返回`text`数据  


```python
>>> import requests
>>> from requests.exceptions import HTTPError
```


```python
>>> def get_data(url):
>>>     
>>>     response = requests.get(url)
>>>     if response.status_code == requests.codes.ok:  # 检测状态码
>>>         return response.text  # 返回响应的文本信息
>>>     else:
>>>         response.raise_for_status()  # 4xx 5xx 时,引出错误 代替 raise requests.exception.HTTPError
```


```python
>>>  url = "https://movie.douban.com/tag/Top100"
```


```python
>>> data = get_data(url)  # 获取数据
>>> data_res = {}  # 存储数据的初始化字典
```

## 3. 提取数据
   - 正则提取
   - BeautifulSoup 提取
   - Xpath 提取
   - pyquery 提取
   - scrapy 混合提取

### 1. 正则提取
- 观察数据位置
![电影名，海报地址](./images/re_name_poster.png)


```python
>>> import re
```

### 提取 海报地址以及电影名称
**通过查看该请求的响应内容快速进行复制匹配,如下图搜索:**
![复制匹配](./images/re_get_data_1.png)  
用到的匹配规则提示:
   - "." 表示任意非空格换行等字符
   - ".*?"  表示贪婪匹配,最少匹配一次
   - "()"  表示提取()中的内容
   -  "\\w" 表示正常字符,比如英文字母,中文等常见文字
   - ".+"  表示至少匹配一次任意字符


```python
>>> # 设置提取表达式 
>>> poster_pattern = re.compile(r"""<a class="nbg" href=".*?"  title=".*?">.*?<img src="(.*?)" width="75" alt="(.*?)" class=""/>.*?</a>""", re.S)  # 海报的正则表达式
movie_name_pattern = re.compile(r""" <div class="pl2">.*? <a href=".*?"  class="">.*?(\w+).*?<span style="font-size:13px;">(.*?)</span>.*?</a>""", re.S)  # 电影名正则表达式
poster_res = re.findall(poster_pattern, data)  # 获取所有匹配结果
movie_name_res = re.findall(movie_name_pattern, data)
poster_res, movie_name_res
```
      ...
      ('https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910902213.jpg',
       '低俗小说'),
      ('https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1665997400.jpg',
       '美丽心灵')],
     [('辛德勒的名单', '舒特拉的名单(港) / 辛德勒名单'),
      ('狩猎', '谎言的烙印(台) / 诬网(港)'),
      ('美国往事', '四海兄弟(台) / 义薄云天(港)'),
      ...

**查看结果好像没什么问题, 我们用长度比较来看看数量是否一致**


```python
len(poster_res) == len(movie_name_res)
```




    True



**长度一致,看来匹配规则在这里没问题**
我们将提取到的数据存储到我们的数据结构`data_res`中


```python
for poster, movie_name in zip(poster_res, movie_name_res):  # 压缩遍历
    # 进行名称验证，是否对应,
    name1 = poster[1]
    name2 = movie_name[0]
    if name1 == name2:
        tmp_dict = data_res.get(name1, {})  # 初始化字典
        tmp_dict.update({"poster": poster[0]})  # 字典更新
        tmp_dict.update({"else_name": movie_name[1]})  # 字典更新
        data_res[name1] = tmp_dict
data_res
```




    {'辛德勒的名单': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p492406163.jpg',
      'else_name': '舒特拉的名单(港) / 辛德勒名单'},
     '狩猎': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1546987967.jpg',
      'else_name': '谎言的烙印(台) / 诬网(港)'},
     '美国往事': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p477229647.jpg',
      'else_name': '四海兄弟(台) / 义薄云天(港)'},
     '十二怒汉': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2173577632.jpg',
      'else_name': '12怒汉 / 十二怒汉'},
     '窃听风暴': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1808872109.jpg',
      'else_name': '窃听者(港) / 他人的生活'},
     '天堂电影院': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910901025.jpg',
      'else_name': '星光伴我心(港) / 新天堂乐园(台)'},
     '教父': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p616779645.jpg',
      'else_name': 'Mario Puzo&#39;s The Godfather'},
     '一一': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2119675128.jpg',
      'else_name': 'Yi yi / Yi yi: A One and a Two'},
     '飞越疯人院': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792238287.jpg',
      'else_name': '飞越杜鹃窝(台) / 飞越喜鹊巢'},
     '鬼子来了': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1181775734.jpg',
      'else_name': 'Devils on the Doorstep'},
     '两杆大烟枪': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792443418.jpg',
      'else_name': '够姜四小强(港) / 两根枪管(台)'},
     '被嫌弃的松子的一生': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p453723669.jpg',
      'else_name': '花样奇缘(港) / 令人讨厌的松子的一生(台)'},
     '活着': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2513253791.jpg',
      'else_name': '人生 / Lifetimes'},
     '楚门的世界': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg',
      'else_name': '真人Show(港) / 真人戏'},
     '搏击俱乐部': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910926158.jpg',
      'else_name': '搏击会(港) / 斗阵俱乐部(台)'},
     '死亡诗社': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910824340.jpg',
      'else_name': '暴雨骄阳(港) / 春风化雨(台)'},
     'V字仇杀队': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1465235231.jpg',
      'else_name': 'V煞(港) / V怪客(台)'},
     '闻香识女人': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2550757929.jpg',
      'else_name': '女人香 / 女人的芳香'},
     '低俗小说': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910902213.jpg',
      'else_name': '黑色追緝令(台) / 危险人物(港)'},
     '美丽心灵': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1665997400.jpg',
      'else_name': '有你终生美丽(港) / 美丽境界(台)'}}



**我们用同样的方法,提取其他需要的数据**  
***这里有个小技巧,用额外的字段来得到唯一匹配, 如下图:***  
需要的数据:  
![需要的数据](./images/unique1.png)   
额外数据匹配:  
![额外匹配](./images/unique2.png)

#### 整体提取
**由于所有数据都集中在一个块，如下图：**  
![总数据](./images/total_data.png)  
所有我们就一次性全部提取，方便数据的收集.  
由于有些是电影值有一个年份，所以匹配不好匹配，我们匹配整体后利用"/"进行分割再挑选.  
*PS: 其实正则匹配这种很多字段的容易出错，换行之类的字符容易忘记替代，所以建议一点一点的增加匹配表达式的长度.*


```python
total_pattern = re.compile("""<p class="ul">.*?<a class="nbg" href=".*?"  title="(.*?)">.*?<img src="(.*?)" width="75".*?<div class="pl2">.*?<a href=".*?"  class="">.*?(\w+).*?style="font-size:13px;">(.*?)</span>.*?class="pl">(.*?)</p>.*?class="star clearfix">.*?"allstar45"></span>.*?"rating_nums">(.*?)</span>.*?<span class="pl">\((.*?)\)</span>.*?<div id=".*?"></div>""", re.S)
res = re.findall(total_pattern, data)
res
```




    [('狩猎',
      'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1546987967.jpg',
      '狩猎',
      '谎言的烙印(台) / 诬网(港)',
      '2012-05-20(戛纳电影节) / 2013-01-10(丹麦) / 麦斯·米科尔森 / 托玛斯·博·拉森 / 安妮卡·韦德科普 / 拉丝·弗格斯托姆 / 苏西·沃德 / 安妮·路易丝·哈辛 / 拉斯·兰特 / 亚历山德拉·拉帕波特 / 拉斯穆斯·林德·鲁宾 / 丹麦 / 瑞典 / 托马斯·温特伯格...',
      '9.1',
      '184560人评价'),
     ('美国往事',
      'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p477229647.jpg',
      '美国往事',
      '四海兄弟(台) / 义薄云天(港)',
      '1984-02-17(波士顿首映) / 1984-09-28(意大利) / 罗伯特·德尼罗 / 詹姆斯·伍兹 / 伊丽莎白·麦戈文 / 乔·佩西 / 波特·杨 / 塔斯黛·韦尔德 / 特里特·威廉斯 / 丹尼·爱罗 / 理查德·布赖特 / 詹姆斯·海登 / 威廉·弗西斯 / 达兰妮·弗鲁格 / 拉里·拉普...',
      '9.1',
      '232940人评价'),
     ('十二怒汉',
      'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2173577632.jpg',
      '十二怒汉',
      '12怒汉 / 十二怒汉',
      '1957-04-13(美国) / 亨利·方达 / 马丁·鲍尔萨姆 / 约翰·菲德勒 / 李·科布 / E.G.马绍尔 / 杰克·克卢格曼  / 爱德华·宾斯 / 杰克·瓦尔登 / 约瑟夫·史威尼 / 埃德·贝格利 / 乔治·沃斯科维奇 / 罗伯特·韦伯 / 美国 / 西德尼·吕美特 / 96 分钟...',
      '9.4',
      '238341人评价'),
     ('窃听风暴',
      'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1808872109.jpg',
      '窃听风暴',
      '窃听者(港) / 他人的生活',
      '2006-03-23(德国) / 乌尔里希·穆埃 / 马蒂娜·格德克 / 塞巴斯蒂安·科赫 / 乌尔里希·图库尔 / 托马斯·蒂梅 / 汉斯-尤韦·鲍尔 / 沃克马·克莱纳特 / 马提亚斯·布伦纳 / 查理·哈纳 / 赫伯特·克瑙普 / 巴斯蒂安·特罗斯特 / 玛丽·格鲁伯...',
      '9.1',
      '317944人评价'),
     ('天堂电影院',
      'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910901025.jpg',
      '天堂电影院',
      '星光伴我心(港) / 新天堂乐园(台)',
      '1988-11-17(意大利) / 安东内拉·阿蒂利 / 恩佐·卡拉瓦勒 / 艾萨·丹尼埃利 / 里奥·故罗塔 / 马克·莱昂纳蒂 / 普佩拉·玛奇奥 / 阿格妮丝·那诺 / 莱奥波多·特里耶斯泰 / 萨瓦特利·卡西欧 / 尼古拉·迪·平托 / 罗伯塔·蕾娜 / 尼诺·戴罗佐...',
      '9.2',
      '396652人评价'),
     ('教父',
      'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p616779645.jpg',
      '教父',
      'Mario Puzo&#39;s The Godfather',
      '1972-03-15(纽约首映) / 1972-03-24(美国) / 马龙·白兰度 / 阿尔·帕西诺 / 詹姆斯·肯恩 / 理查德·卡斯特尔诺 / 罗伯特·杜瓦尔 / 斯特林·海登 / 约翰·马利 / 理查德·康特 / 艾尔·勒提埃里 / 黛安·基顿 / 阿贝·维高达 / 塔莉娅·夏尔 / 吉亚尼·罗素...',
      '9.2',
      '496913人评价'),
     ('一一',
      'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2119675128.jpg',
      '一一',
      'Yi yi / Yi yi: A One and a Two',
      '2000-05-14(戛纳电影节) / 2000-12-16(日本) / 2017-07-28(台湾) / 李凯莉 / 金燕玲 / 张洋洋 / 萧淑慎 / 尾形一成 / 陈希圣 / 林孟瑾 / 陈以文 / 柯宇纶 / 柯素云 / 唐如韫 / 徐淑媛 / 陶传正 / 孙法钧 / 津田健次郎 / 江惠惠 / 李永丰 / 许安安 / 戴立忍...',
      '9.0',
      '199330人评价'),
     ('飞越疯人院',
      'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792238287.jpg',
      '飞越疯人院',
      '飞越杜鹃窝(台) / 飞越喜鹊巢',
      '1975-11-19(美国) / 杰克·尼科尔森 / 丹尼·德维托 / 克里斯托弗·洛伊德 / 路易丝·弗莱彻 / 威尔·萨姆森 / 特德·马克兰德 / 布拉德·道里夫 / 斯加特曼·克罗索斯 / 迈克尔·贝里曼 / 彼得·布罗科 / 穆瓦科·卡姆布卡 / 威廉·达尔 / 乔西普·艾利克...',
      '9.1',
      '354920人评价'),
     ('鬼子来了',
      'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1181775734.jpg',
      '鬼子来了',
      'Devils on the Doorstep',
      '2000-05-12(戛纳电影节) / 2002-04-27(日本) / 姜文 / 香川照之 / 袁丁 / 姜宏波 / 丛志军 / 喜子 / 泽田谦也 / 李海滨 / 蔡卫东 / 陈述 / 陈莲梅 / 史建全 / 陈强 / 宫路佳具 / 吴大维 / 梶冈润一 / 石山雄大 / 述平 / 姜武 / 中国大陆 / 姜文 / 139分钟...',
      '9.2',
      '334681人评价'),
     ('两杆大烟枪',
      'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792443418.jpg',
      '两杆大烟枪',
      '够姜四小强(港) / 两根枪管(台)',
      '1998-08-28(英国) / 杰森·弗莱明 / 德克斯特·弗莱彻 / 尼克·莫兰 / 杰森·斯坦森 / 斯蒂文·麦金托什 / 斯汀 / 维尼·琼斯 / 丹尼·约翰-儒勒 / 维克多·麦奎尔 / 阿兰·福德 / 安德鲁·蒂曼 / 马修·沃恩 / 弗兰克·哈珀 / 罗尼·福克斯 / 罗伯·布莱顿...',
      '9.1',
      '352235人评价'),
     ('被嫌弃的松子的一生',
      'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p453723669.jpg',
      '被嫌弃的松子的一生',
      '花样奇缘(港) / 令人讨厌的松子的一生(台)',
      '2006-05-27(日本) / 中谷美纪 / 瑛太 / 香川照之 / 市川实日子 / 伊势谷友介 / 柄本明 / 黑泽明日香 / 荒川良良 / 柴崎幸 / 土屋安娜 / 奥之矢佳奈 / 谷原章介 / 武田真治 / 片平渚 / 宫藤官九郎 / 角野卓造 / 田中要次 / 木村凯拉 / 谷中敦...',
      '8.9',
      '414122人评价'),
     ('活着',
      'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2513253791.jpg',
      '活着',
      '人生 / Lifetimes',
      '1994-05-17(戛纳电影节) / 1994-06-30(香港) / 葛优 / 巩俐 / 姜武 / 牛犇 / 郭涛 / 张璐 / 倪大红 / 肖聪 / 董飞 / 刘天池 / 董立范 / 黄宗洛 / 刘燕瑾 / 李连义 / 杨同顺 / 苏岩 / 王丽华 / 中国大陆 / 香港 / 张艺谋 / 132分钟 / 剧情 / 历史 / 家庭...',
      '9.2',
      '409160人评价'),
     ('楚门的世界',
      'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg',
      '楚门的世界',
      '真人Show(港) / 真人戏',
      '1998-06-05(美国) / 金·凯瑞 / 劳拉·琳妮 / 艾德·哈里斯 / 诺亚·艾默里奇 / 娜塔莎·麦克艾霍恩 / 马西娅·德波尼斯 / Adam Tomei / 哈里·谢尔 / 约翰·普莱舍 / 澳澜·琼斯 / Joe Minjares / 特里·金瑞利 / 乔尔·麦金农·米勒 / 冈本玉二 / Jake Eberle...',
      '9.2',
      '755718人评价'),
     ('搏击俱乐部',
      'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910926158.jpg',
      '搏击俱乐部',
      '搏击会(港) / 斗阵俱乐部(台)',
      '1999-09-10(威尼斯电影节) / 1999-10-15(美国) / 爱德华·诺顿 / 布拉德·皮特 / 海伦娜·伯翰·卡特 / 扎克·格雷尼尔 / 米特·洛夫 / 杰瑞德·莱托 / 艾恩·贝利 / 里奇蒙德·阿奎特  / 乔治·马奎尔 / 鲍勃·斯蒂芬森 / Carl Ciarfalio / 斯图尔特·布拉姆博格...',
      '9.0',
      '514373人评价'),
     ('死亡诗社',
      'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910824340.jpg',
      '死亡诗社',
      '暴雨骄阳(港) / 春风化雨(台)',
      '1989-06-02(多伦多首映) / 1989-06-09(美国) / 罗宾·威廉姆斯 / 罗伯特·肖恩·莱纳德 / 伊桑·霍克 / 乔西·查尔斯 / 盖尔·汉森 / 迪伦·库斯曼 / 阿勒隆·鲁杰罗 / 詹姆斯·沃特斯顿 / 诺曼·劳埃德 / 柯特伍德·史密斯 / 卡拉·贝尔韦尔 / 利昂·波纳尔...',
      '9.0',
      '388695人评价'),
     ('V字仇杀队',
      'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1465235231.jpg',
      'V字仇杀队',
      'V煞(港) / V怪客(台)',
      '2005-12-11(BNAT电影节) / 2006-03-17(美国) / 娜塔莉·波特曼 / 雨果·维文 / 斯蒂芬·瑞 / 斯蒂芬·弗雷 / 约翰·赫特 / 蒂姆·皮戈特-史密斯 / 鲁珀特·格雷夫斯 / 罗杰·阿拉姆 / 本·迈尔斯 / 西妮德·库萨克 / 娜塔莎·怀特曼 / 约翰·斯坦丁 /...',
      '8.8',
      '593760人评价'),
     ('闻香识女人',
      'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2550757929.jpg',
      '闻香识女人',
      '女人香 / 女人的芳香',
      '1992-12-23(美国) / 阿尔·帕西诺 / 克里斯·奥唐纳 / 詹姆斯·瑞布霍恩 / 加布里埃尔·安瓦尔 / 菲利普·塞默·霍夫曼 / 理查德·文彻 / 布莱德利·惠特福德 / 罗谢尔·奥利弗 / 托德·路易斯 / 马特·史密斯 / 吉恩·坎菲尔德 / 弗兰西丝·康罗伊...',
      '9.0',
      '457858人评价'),
     ('低俗小说',
      'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910902213.jpg',
      '低俗小说',
      '黑色追緝令(台) / 危险人物(港)',
      '1994-05-12(戛纳电影节) / 1994-10-14(美国) / 约翰·特拉沃尔塔 / 乌玛·瑟曼 / 阿曼达·普拉莫 / 蒂姆·罗斯 / 塞缪尔·杰克逊 / 菲尔·拉马 / 布鲁斯·威利斯 / 弗兰克·威利 / 布尔·斯蒂尔斯 / 文·瑞姆斯 / 劳拉·拉芙蕾丝 / 保罗·考尔德伦...',
      '8.8',
      '460328人评价'),
     ('美丽心灵',
      'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1665997400.jpg',
      '美丽心灵',
      '有你终生美丽(港) / 美丽境界(台)',
      '2001-12-13(加州首映) / 2002-01-04(美国) / 罗素·克劳 / 艾德·哈里斯 / 詹妮弗·康纳利 / 克里斯托弗·普卢默 / 保罗·贝坦尼 / 亚当·戈德堡 / 乔什·卢卡斯 / 安东尼·拉普 / 贾森·加里-斯坦福德 / 贾德·赫希 / 奥斯汀·潘德尔顿 / 薇薇·卡登尼...',
      '8.9',
      '411983人评价')]



#### 观察整体数据情况，提取数据  
![需要稍复杂处理](./images/time_handle.png)


```python
def get_time_actor(data):
    """
    获取处理后的时间和演员数据
    :param data: 
    :return: 
    """
    tmp_data = data.split(" / ")
    ind = 1
    for i, v in enumerate(tmp_data):
        if v[:4].isdigit():  # 判断是否为数字
            ind += 1
        else:
            break
        return tmp_data[:ind], tmp_data[ind:]
```


```python
for tmp_data in res:
    tmp = data_res.get(tmp_data[0], {})  # 获取原来的字典数据
    if tmp_data[0] == tmp_data[2]:  # 检测数据是否对齐
        tmp.update({"movie_name": tmp_data[0], "poster_url": tmp_data[1], "other_name": tmp_data[3], "score": float(tmp_data[-2]), "comment_people": tmp_data[-1].replace("人评价", "")})  # 更新数据
        time_data, actor = get_time_actor(tmp_data[-3])
        tmp.update({"release_time": time_data, "actor": actor})
        data_res[tmp_data[0]] = tmp
    else:
        print("数据有误")
print(data_res)
```

    {'辛德勒的名单': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p492406163.jpg', 'else_name': '舒特拉的名单(港) / 辛德勒名单'}, '狩猎': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1546987967.jpg', 'else_name': '谎言的烙印(台) / 诬网(港)', 'movie_name': '狩猎', 'poster_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1546987967.jpg', 'other_name': '谎言的烙印(台) / 诬网(港)', 'score': 9.1, 'comment_people': '184560', 'release_time': ['2012-05-20(戛纳电影节)', '2013-01-10(丹麦)'], 'actor': ['麦斯·米科尔森', '托玛斯·博·拉森', '安妮卡·韦德科普', '拉丝·弗格斯托姆', '苏西·沃德', '安妮·路易丝·哈辛', '拉斯·兰特', '亚历山德拉·拉帕波特', '拉斯穆斯·林德·鲁宾', '丹麦', '瑞典', '托马斯·温特伯格...']}, '美国往事': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p477229647.jpg', 'else_name': '四海兄弟(台) / 义薄云天(港)', 'movie_name': '美国往事', 'poster_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p477229647.jpg', 'other_name': '四海兄弟(台) / 义薄云天(港)', 'score': 9.1, 'comment_people': '232940', 'release_time': ['1984-02-17(波士顿首映)', '1984-09-28(意大利)'], 'actor': ['罗伯特·德尼罗', '詹姆斯·伍兹', '伊丽莎白·麦戈文', '乔·佩西', '波特·杨', '塔斯黛·韦尔德', '特里特·威廉斯', '丹尼·爱罗', '理查德·布赖特', '詹姆斯·海登', '威廉·弗西斯', '达兰妮·弗鲁格', '拉里·拉普...']}, '十二怒汉': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2173577632.jpg', 'else_name': '12怒汉 / 十二怒汉', 'movie_name': '十二怒汉', 'poster_url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2173577632.jpg', 'other_name': '12怒汉 / 十二怒汉', 'score': 9.4, 'comment_people': '238341', 'release_time': ['1957-04-13(美国)', '亨利·方达'], 'actor': ['马丁·鲍尔萨姆', '约翰·菲德勒', '李·科布', 'E.G.马绍尔', '杰克·克卢格曼 ', '爱德华·宾斯', '杰克·瓦尔登', '约瑟夫·史威尼', '埃德·贝格利', '乔治·沃斯科维奇', '罗伯特·韦伯', '美国', '西德尼·吕美特', '96 分钟...']}, '窃听风暴': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1808872109.jpg', 'else_name': '窃听者(港) / 他人的生活', 'movie_name': '窃听风暴', 'poster_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1808872109.jpg', 'other_name': '窃听者(港) / 他人的生活', 'score': 9.1, 'comment_people': '317944', 'release_time': ['2006-03-23(德国)', '乌尔里希·穆埃'], 'actor': ['马蒂娜·格德克', '塞巴斯蒂安·科赫', '乌尔里希·图库尔', '托马斯·蒂梅', '汉斯-尤韦·鲍尔', '沃克马·克莱纳特', '马提亚斯·布伦纳', '查理·哈纳', '赫伯特·克瑙普', '巴斯蒂安·特罗斯特', '玛丽·格鲁伯...']}, '天堂电影院': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910901025.jpg', 'else_name': '星光伴我心(港) / 新天堂乐园(台)', 'movie_name': '天堂电影院', 'poster_url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910901025.jpg', 'other_name': '星光伴我心(港) / 新天堂乐园(台)', 'score': 9.2, 'comment_people': '396652', 'release_time': ['1988-11-17(意大利)', '安东内拉·阿蒂利'], 'actor': ['恩佐·卡拉瓦勒', '艾萨·丹尼埃利', '里奥·故罗塔', '马克·莱昂纳蒂', '普佩拉·玛奇奥', '阿格妮丝·那诺', '莱奥波多·特里耶斯泰', '萨瓦特利·卡西欧', '尼古拉·迪·平托', '罗伯塔·蕾娜', '尼诺·戴罗佐...']}, '教父': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p616779645.jpg', 'else_name': 'Mario Puzo&#39;s The Godfather', 'movie_name': '教父', 'poster_url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p616779645.jpg', 'other_name': 'Mario Puzo&#39;s The Godfather', 'score': 9.2, 'comment_people': '496913', 'release_time': ['1972-03-15(纽约首映)', '1972-03-24(美国)'], 'actor': ['马龙·白兰度', '阿尔·帕西诺', '詹姆斯·肯恩', '理查德·卡斯特尔诺', '罗伯特·杜瓦尔', '斯特林·海登', '约翰·马利', '理查德·康特', '艾尔·勒提埃里', '黛安·基顿', '阿贝·维高达', '塔莉娅·夏尔', '吉亚尼·罗素...']}, '一一': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2119675128.jpg', 'else_name': 'Yi yi / Yi yi: A One and a Two', 'movie_name': '一一', 'poster_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2119675128.jpg', 'other_name': 'Yi yi / Yi yi: A One and a Two', 'score': 9.0, 'comment_people': '199330', 'release_time': ['2000-05-14(戛纳电影节)', '2000-12-16(日本)'], 'actor': ['2017-07-28(台湾)', '李凯莉', '金燕玲', '张洋洋', '萧淑慎', '尾形一成', '陈希圣', '林孟瑾', '陈以文', '柯宇纶', '柯素云', '唐如韫', '徐淑媛', '陶传正', '孙法钧', '津田健次郎', '江惠惠', '李永丰', '许安安', '戴立忍...']}, '飞越疯人院': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792238287.jpg', 'else_name': '飞越杜鹃窝(台) / 飞越喜鹊巢', 'movie_name': '飞越疯人院', 'poster_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792238287.jpg', 'other_name': '飞越杜鹃窝(台) / 飞越喜鹊巢', 'score': 9.1, 'comment_people': '354920', 'release_time': ['1975-11-19(美国)', '杰克·尼科尔森'], 'actor': ['丹尼·德维托', '克里斯托弗·洛伊德', '路易丝·弗莱彻', '威尔·萨姆森', '特德·马克兰德', '布拉德·道里夫', '斯加特曼·克罗索斯', '迈克尔·贝里曼', '彼得·布罗科', '穆瓦科·卡姆布卡', '威廉·达尔', '乔西普·艾利克...']}, '鬼子来了': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1181775734.jpg', 'else_name': 'Devils on the Doorstep', 'movie_name': '鬼子来了', 'poster_url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1181775734.jpg', 'other_name': 'Devils on the Doorstep', 'score': 9.2, 'comment_people': '334681', 'release_time': ['2000-05-12(戛纳电影节)', '2002-04-27(日本)'], 'actor': ['姜文', '香川照之', '袁丁', '姜宏波', '丛志军', '喜子', '泽田谦也', '李海滨', '蔡卫东', '陈述', '陈莲梅', '史建全', '陈强', '宫路佳具', '吴大维', '梶冈润一', '石山雄大', '述平', '姜武', '中国大陆', '姜文', '139分钟...']}, '两杆大烟枪': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792443418.jpg', 'else_name': '够姜四小强(港) / 两根枪管(台)', 'movie_name': '两杆大烟枪', 'poster_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792443418.jpg', 'other_name': '够姜四小强(港) / 两根枪管(台)', 'score': 9.1, 'comment_people': '352235', 'release_time': ['1998-08-28(英国)', '杰森·弗莱明'], 'actor': ['德克斯特·弗莱彻', '尼克·莫兰', '杰森·斯坦森', '斯蒂文·麦金托什', '斯汀', '维尼·琼斯', '丹尼·约翰-儒勒', '维克多·麦奎尔', '阿兰·福德', '安德鲁·蒂曼', '马修·沃恩', '弗兰克·哈珀', '罗尼·福克斯', '罗伯·布莱顿...']}, '被嫌弃的松子的一生': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p453723669.jpg', 'else_name': '花样奇缘(港) / 令人讨厌的松子的一生(台)', 'movie_name': '被嫌弃的松子的一生', 'poster_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p453723669.jpg', 'other_name': '花样奇缘(港) / 令人讨厌的松子的一生(台)', 'score': 8.9, 'comment_people': '414122', 'release_time': ['2006-05-27(日本)', '中谷美纪'], 'actor': ['瑛太', '香川照之', '市川实日子', '伊势谷友介', '柄本明', '黑泽明日香', '荒川良良', '柴崎幸', '土屋安娜', '奥之矢佳奈', '谷原章介', '武田真治', '片平渚', '宫藤官九郎', '角野卓造', '田中要次', '木村凯拉', '谷中敦...']}, '活着': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2513253791.jpg', 'else_name': '人生 / Lifetimes', 'movie_name': '活着', 'poster_url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2513253791.jpg', 'other_name': '人生 / Lifetimes', 'score': 9.2, 'comment_people': '409160', 'release_time': ['1994-05-17(戛纳电影节)', '1994-06-30(香港)'], 'actor': ['葛优', '巩俐', '姜武', '牛犇', '郭涛', '张璐', '倪大红', '肖聪', '董飞', '刘天池', '董立范', '黄宗洛', '刘燕瑾', '李连义', '杨同顺', '苏岩', '王丽华', '中国大陆', '香港', '张艺谋', '132分钟', '剧情', '历史', '家庭...']}, '楚门的世界': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg', 'else_name': '真人Show(港) / 真人戏', 'movie_name': '楚门的世界', 'poster_url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg', 'other_name': '真人Show(港) / 真人戏', 'score': 9.2, 'comment_people': '755718', 'release_time': ['1998-06-05(美国)', '金·凯瑞'], 'actor': ['劳拉·琳妮', '艾德·哈里斯', '诺亚·艾默里奇', '娜塔莎·麦克艾霍恩', '马西娅·德波尼斯', 'Adam Tomei', '哈里·谢尔', '约翰·普莱舍', '澳澜·琼斯', 'Joe Minjares', '特里·金瑞利', '乔尔·麦金农·米勒', '冈本玉二', 'Jake Eberle...']}, '搏击俱乐部': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910926158.jpg', 'else_name': '搏击会(港) / 斗阵俱乐部(台)', 'movie_name': '搏击俱乐部', 'poster_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910926158.jpg', 'other_name': '搏击会(港) / 斗阵俱乐部(台)', 'score': 9.0, 'comment_people': '514373', 'release_time': ['1999-09-10(威尼斯电影节)', '1999-10-15(美国)'], 'actor': ['爱德华·诺顿', '布拉德·皮特', '海伦娜·伯翰·卡特', '扎克·格雷尼尔', '米特·洛夫', '杰瑞德·莱托', '艾恩·贝利', '里奇蒙德·阿奎特 ', '乔治·马奎尔', '鲍勃·斯蒂芬森', 'Carl Ciarfalio', '斯图尔特·布拉姆博格...']}, '死亡诗社': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910824340.jpg', 'else_name': '暴雨骄阳(港) / 春风化雨(台)', 'movie_name': '死亡诗社', 'poster_url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910824340.jpg', 'other_name': '暴雨骄阳(港) / 春风化雨(台)', 'score': 9.0, 'comment_people': '388695', 'release_time': ['1989-06-02(多伦多首映)', '1989-06-09(美国)'], 'actor': ['罗宾·威廉姆斯', '罗伯特·肖恩·莱纳德', '伊桑·霍克', '乔西·查尔斯', '盖尔·汉森', '迪伦·库斯曼', '阿勒隆·鲁杰罗', '詹姆斯·沃特斯顿', '诺曼·劳埃德', '柯特伍德·史密斯', '卡拉·贝尔韦尔', '利昂·波纳尔...']}, 'V字仇杀队': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1465235231.jpg', 'else_name': 'V煞(港) / V怪客(台)', 'movie_name': 'V字仇杀队', 'poster_url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1465235231.jpg', 'other_name': 'V煞(港) / V怪客(台)', 'score': 8.8, 'comment_people': '593760', 'release_time': ['2005-12-11(BNAT电影节)', '2006-03-17(美国)'], 'actor': ['娜塔莉·波特曼', '雨果·维文', '斯蒂芬·瑞', '斯蒂芬·弗雷', '约翰·赫特', '蒂姆·皮戈特-史密斯', '鲁珀特·格雷夫斯', '罗杰·阿拉姆', '本·迈尔斯', '西妮德·库萨克', '娜塔莎·怀特曼', '约翰·斯坦丁 /...']}, '闻香识女人': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2550757929.jpg', 'else_name': '女人香 / 女人的芳香', 'movie_name': '闻香识女人', 'poster_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2550757929.jpg', 'other_name': '女人香 / 女人的芳香', 'score': 9.0, 'comment_people': '457858', 'release_time': ['1992-12-23(美国)', '阿尔·帕西诺'], 'actor': ['克里斯·奥唐纳', '詹姆斯·瑞布霍恩', '加布里埃尔·安瓦尔', '菲利普·塞默·霍夫曼', '理查德·文彻', '布莱德利·惠特福德', '罗谢尔·奥利弗', '托德·路易斯', '马特·史密斯', '吉恩·坎菲尔德', '弗兰西丝·康罗伊...']}, '低俗小说': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910902213.jpg', 'else_name': '黑色追緝令(台) / 危险人物(港)', 'movie_name': '低俗小说', 'poster_url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910902213.jpg', 'other_name': '黑色追緝令(台) / 危险人物(港)', 'score': 8.8, 'comment_people': '460328', 'release_time': ['1994-05-12(戛纳电影节)', '1994-10-14(美国)'], 'actor': ['约翰·特拉沃尔塔', '乌玛·瑟曼', '阿曼达·普拉莫', '蒂姆·罗斯', '塞缪尔·杰克逊', '菲尔·拉马', '布鲁斯·威利斯', '弗兰克·威利', '布尔·斯蒂尔斯', '文·瑞姆斯', '劳拉·拉芙蕾丝', '保罗·考尔德伦...']}, '美丽心灵': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1665997400.jpg', 'else_name': '有你终生美丽(港) / 美丽境界(台)', 'movie_name': '美丽心灵', 'poster_url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1665997400.jpg', 'other_name': '有你终生美丽(港) / 美丽境界(台)', 'score': 8.9, 'comment_people': '411983', 'release_time': ['2001-12-13(加州首映)', '2002-01-04(美国)'], 'actor': ['罗素·克劳', '艾德·哈里斯', '詹妮弗·康纳利', '克里斯托弗·普卢默', '保罗·贝坦尼', '亚当·戈德堡', '乔什·卢卡斯', '安东尼·拉普', '贾森·加里-斯坦福德', '贾德·赫希', '奥斯汀·潘德尔顿', '薇薇·卡登尼...']}}


## 2. BeautifulSoup （css选择器） 提取


```python
from bs4 import BeautifulSoup
```


```python
soup = BeautifulSoup(data, "lxml")  # 初始化soup对象
```

#### 利用css选择器逐一获取数据
**poster**: `".nbg img"`  
**movie_name**: `".pl2 a"`  
**time_actor**: `".pl2 p.pl"`  
**score**: `".rating_nums"`  
**comment_people**: `".star.clearfix .pl"`   


***PS:***  
- "." 表示class 
- " "表示子孙节点  
- img 就是img节点  
- a 就是a节点
- "#abd" 表示 id="abc"的节点


```python
poster = soup.select(".nbg img")  # 海报
movie_name = soup.select(".pl2 a")  # 电影名称
time_actor = soup.select(".pl2 p.pl")  # 上映时间及演员
score = soup.select(".rating_nums")  # 电影评分
comment_people = soup.select(".star.clearfix .pl")  # 评分人数
movie_data = {}  # 存储结构
```

#### 批量获取数据


```python
for p, m, t, s, c in zip(poster, movie_name, time_actor, score, comment_people):
    pos = p.get("src")  # 海报地址
    mov = m.get_text().replace(m.select("span")[0].get_text(), "")  # 电影名称
    mov = mov.replace("/", "").strip()  # 去掉不需要的字符
    other_name = m.select("span")[0].get_text()  # 额外名字
    release_time, actor = get_time_actor(t.get_text())
    sco = s.get_text()
    comment = c.get_text()
    movie_data.update({mov: {"poster": pos, "movie_name": mov, "other_name": other_name, "release_time": release_time, "actor": actor, "score": sco, "comment": comment}})
print(movie_data)
```

    {'辛德勒的名单': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p492406163.jpg', 'movie_name': '辛德勒的名单', 'other_name': '舒特拉的名单(港) / 辛德勒名单', 'release_time': ['1993-11-30(华盛顿首映)', '1994-02-04(美国)'], 'actor': ['连姆·尼森', '本·金斯利', '拉尔夫·费因斯', '卡罗琳·古多尔', '乔纳森·萨加尔', '艾伯丝·戴维兹', '马尔戈萨·格贝尔', '马克·伊瓦涅', '碧翠斯·马科拉', '安德烈·瑟韦林', '弗里德里希·冯·图恩', '克齐斯茨托夫·拉夫特...'], 'score': '9.5', 'comment': '(571888人评价)'}, '狩猎': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1546987967.jpg', 'movie_name': '狩猎', 'other_name': '谎言的烙印(台) / 诬网(港)', 'release_time': ['2012-05-20(戛纳电影节)', '2013-01-10(丹麦)'], 'actor': ['麦斯·米科尔森', '托玛斯·博·拉森', '安妮卡·韦德科普', '拉丝·弗格斯托姆', '苏西·沃德', '安妮·路易丝·哈辛', '拉斯·兰特', '亚历山德拉·拉帕波特', '拉斯穆斯·林德·鲁宾', '丹麦', '瑞典', '托马斯·温特伯格...'], 'score': '9.1', 'comment': '(184560人评价)'}, '美国往事': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p477229647.jpg', 'movie_name': '美国往事', 'other_name': '四海兄弟(台) / 义薄云天(港)', 'release_time': ['1984-02-17(波士顿首映)', '1984-09-28(意大利)'], 'actor': ['罗伯特·德尼罗', '詹姆斯·伍兹', '伊丽莎白·麦戈文', '乔·佩西', '波特·杨', '塔斯黛·韦尔德', '特里特·威廉斯', '丹尼·爱罗', '理查德·布赖特', '詹姆斯·海登', '威廉·弗西斯', '达兰妮·弗鲁格', '拉里·拉普...'], 'score': '9.1', 'comment': '(232940人评价)'}, '十二怒汉': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2173577632.jpg', 'movie_name': '十二怒汉', 'other_name': '12怒汉 / 十二怒汉', 'release_time': ['1957-04-13(美国)', '亨利·方达'], 'actor': ['马丁·鲍尔萨姆', '约翰·菲德勒', '李·科布', 'E.G.马绍尔', '杰克·克卢格曼 ', '爱德华·宾斯', '杰克·瓦尔登', '约瑟夫·史威尼', '埃德·贝格利', '乔治·沃斯科维奇', '罗伯特·韦伯', '美国', '西德尼·吕美特', '96 分钟...'], 'score': '9.4', 'comment': '(238341人评价)'}, '窃听风暴': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1808872109.jpg', 'movie_name': '窃听风暴', 'other_name': '窃听者(港) / 他人的生活', 'release_time': ['2006-03-23(德国)', '乌尔里希·穆埃'], 'actor': ['马蒂娜·格德克', '塞巴斯蒂安·科赫', '乌尔里希·图库尔', '托马斯·蒂梅', '汉斯-尤韦·鲍尔', '沃克马·克莱纳特', '马提亚斯·布伦纳', '查理·哈纳', '赫伯特·克瑙普', '巴斯蒂安·特罗斯特', '玛丽·格鲁伯...'], 'score': '9.1', 'comment': '(317944人评价)'}, '天堂电影院': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910901025.jpg', 'movie_name': '天堂电影院', 'other_name': '星光伴我心(港) / 新天堂乐园(台)', 'release_time': ['1988-11-17(意大利)', '安东内拉·阿蒂利'], 'actor': ['恩佐·卡拉瓦勒', '艾萨·丹尼埃利', '里奥·故罗塔', '马克·莱昂纳蒂', '普佩拉·玛奇奥', '阿格妮丝·那诺', '莱奥波多·特里耶斯泰', '萨瓦特利·卡西欧', '尼古拉·迪·平托', '罗伯塔·蕾娜', '尼诺·戴罗佐...'], 'score': '9.2', 'comment': '(396652人评价)'}, '教父': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p616779645.jpg', 'movie_name': '教父', 'other_name': "Mario Puzo's The Godfather", 'release_time': ['1972-03-15(纽约首映)', '1972-03-24(美国)'], 'actor': ['马龙·白兰度', '阿尔·帕西诺', '詹姆斯·肯恩', '理查德·卡斯特尔诺', '罗伯特·杜瓦尔', '斯特林·海登', '约翰·马利', '理查德·康特', '艾尔·勒提埃里', '黛安·基顿', '阿贝·维高达', '塔莉娅·夏尔', '吉亚尼·罗素...'], 'score': '9.2', 'comment': '(496913人评价)'}, '一一': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2119675128.jpg', 'movie_name': '一一', 'other_name': 'Yi yi / Yi yi: A One and a Two', 'release_time': ['2000-05-14(戛纳电影节)', '2000-12-16(日本)'], 'actor': ['2017-07-28(台湾)', '李凯莉', '金燕玲', '张洋洋', '萧淑慎', '尾形一成', '陈希圣', '林孟瑾', '陈以文', '柯宇纶', '柯素云', '唐如韫', '徐淑媛', '陶传正', '孙法钧', '津田健次郎', '江惠惠', '李永丰', '许安安', '戴立忍...'], 'score': '9.0', 'comment': '(199330人评价)'}, '飞越疯人院': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792238287.jpg', 'movie_name': '飞越疯人院', 'other_name': '飞越杜鹃窝(台) / 飞越喜鹊巢', 'release_time': ['1975-11-19(美国)', '杰克·尼科尔森'], 'actor': ['丹尼·德维托', '克里斯托弗·洛伊德', '路易丝·弗莱彻', '威尔·萨姆森', '特德·马克兰德', '布拉德·道里夫', '斯加特曼·克罗索斯', '迈克尔·贝里曼', '彼得·布罗科', '穆瓦科·卡姆布卡', '威廉·达尔', '乔西普·艾利克...'], 'score': '9.1', 'comment': '(354920人评价)'}, '鬼子来了': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1181775734.jpg', 'movie_name': '鬼子来了', 'other_name': 'Devils on the Doorstep', 'release_time': ['2000-05-12(戛纳电影节)', '2002-04-27(日本)'], 'actor': ['姜文', '香川照之', '袁丁', '姜宏波', '丛志军', '喜子', '泽田谦也', '李海滨', '蔡卫东', '陈述', '陈莲梅', '史建全', '陈强', '宫路佳具', '吴大维', '梶冈润一', '石山雄大', '述平', '姜武', '中国大陆', '姜文', '139分钟...'], 'score': '9.2', 'comment': '(334681人评价)'}, '两杆大烟枪': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792443418.jpg', 'movie_name': '两杆大烟枪', 'other_name': '够姜四小强(港) / 两根枪管(台)', 'release_time': ['1998-08-28(英国)', '杰森·弗莱明'], 'actor': ['德克斯特·弗莱彻', '尼克·莫兰', '杰森·斯坦森', '斯蒂文·麦金托什', '斯汀', '维尼·琼斯', '丹尼·约翰-儒勒', '维克多·麦奎尔', '阿兰·福德', '安德鲁·蒂曼', '马修·沃恩', '弗兰克·哈珀', '罗尼·福克斯', '罗伯·布莱顿...'], 'score': '9.1', 'comment': '(352235人评价)'}, '被嫌弃的松子的一生': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p453723669.jpg', 'movie_name': '被嫌弃的松子的一生', 'other_name': '花样奇缘(港) / 令人讨厌的松子的一生(台)', 'release_time': ['2006-05-27(日本)', '中谷美纪'], 'actor': ['瑛太', '香川照之', '市川实日子', '伊势谷友介', '柄本明', '黑泽明日香', '荒川良良', '柴崎幸', '土屋安娜', '奥之矢佳奈', '谷原章介', '武田真治', '片平渚', '宫藤官九郎', '角野卓造', '田中要次', '木村凯拉', '谷中敦...'], 'score': '8.9', 'comment': '(414122人评价)'}, '活着': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2513253791.jpg', 'movie_name': '活着', 'other_name': '人生 / Lifetimes', 'release_time': ['1994-05-17(戛纳电影节)', '1994-06-30(香港)'], 'actor': ['葛优', '巩俐', '姜武', '牛犇', '郭涛', '张璐', '倪大红', '肖聪', '董飞', '刘天池', '董立范', '黄宗洛', '刘燕瑾', '李连义', '杨同顺', '苏岩', '王丽华', '中国大陆', '香港', '张艺谋', '132分钟', '剧情', '历史', '家庭...'], 'score': '9.2', 'comment': '(409160人评价)'}, '楚门的世界': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg', 'movie_name': '楚门的世界', 'other_name': '真人Show(港) / 真人戏', 'release_time': ['1998-06-05(美国)', '金·凯瑞'], 'actor': ['劳拉·琳妮', '艾德·哈里斯', '诺亚·艾默里奇', '娜塔莎·麦克艾霍恩', '马西娅·德波尼斯', 'Adam Tomei', '哈里·谢尔', '约翰·普莱舍', '澳澜·琼斯', 'Joe Minjares', '特里·金瑞利', '乔尔·麦金农·米勒', '冈本玉二', 'Jake Eberle...'], 'score': '9.2', 'comment': '(755718人评价)'}, '搏击俱乐部': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910926158.jpg', 'movie_name': '搏击俱乐部', 'other_name': '搏击会(港) / 斗阵俱乐部(台)', 'release_time': ['1999-09-10(威尼斯电影节)', '1999-10-15(美国)'], 'actor': ['爱德华·诺顿', '布拉德·皮特', '海伦娜·伯翰·卡特', '扎克·格雷尼尔', '米特·洛夫', '杰瑞德·莱托', '艾恩·贝利', '里奇蒙德·阿奎特 ', '乔治·马奎尔', '鲍勃·斯蒂芬森', 'Carl Ciarfalio', '斯图尔特·布拉姆博格...'], 'score': '9.0', 'comment': '(514373人评价)'}, '死亡诗社': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910824340.jpg', 'movie_name': '死亡诗社', 'other_name': '暴雨骄阳(港) / 春风化雨(台)', 'release_time': ['1989-06-02(多伦多首映)', '1989-06-09(美国)'], 'actor': ['罗宾·威廉姆斯', '罗伯特·肖恩·莱纳德', '伊桑·霍克', '乔西·查尔斯', '盖尔·汉森', '迪伦·库斯曼', '阿勒隆·鲁杰罗', '詹姆斯·沃特斯顿', '诺曼·劳埃德', '柯特伍德·史密斯', '卡拉·贝尔韦尔', '利昂·波纳尔...'], 'score': '9.0', 'comment': '(388695人评价)'}, 'V字仇杀队': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1465235231.jpg', 'movie_name': 'V字仇杀队', 'other_name': 'V煞(港) / V怪客(台)', 'release_time': ['2005-12-11(BNAT电影节)', '2006-03-17(美国)'], 'actor': ['娜塔莉·波特曼', '雨果·维文', '斯蒂芬·瑞', '斯蒂芬·弗雷', '约翰·赫特', '蒂姆·皮戈特-史密斯', '鲁珀特·格雷夫斯', '罗杰·阿拉姆', '本·迈尔斯', '西妮德·库萨克', '娜塔莎·怀特曼', '约翰·斯坦丁 /...'], 'score': '8.8', 'comment': '(593760人评价)'}, '闻香识女人': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2550757929.jpg', 'movie_name': '闻香识女人', 'other_name': '女人香 / 女人的芳香', 'release_time': ['1992-12-23(美国)', '阿尔·帕西诺'], 'actor': ['克里斯·奥唐纳', '詹姆斯·瑞布霍恩', '加布里埃尔·安瓦尔', '菲利普·塞默·霍夫曼', '理查德·文彻', '布莱德利·惠特福德', '罗谢尔·奥利弗', '托德·路易斯', '马特·史密斯', '吉恩·坎菲尔德', '弗兰西丝·康罗伊...'], 'score': '9.0', 'comment': '(457858人评价)'}, '低俗小说': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910902213.jpg', 'movie_name': '低俗小说', 'other_name': '黑色追緝令(台) / 危险人物(港)', 'release_time': ['1994-05-12(戛纳电影节)', '1994-10-14(美国)'], 'actor': ['约翰·特拉沃尔塔', '乌玛·瑟曼', '阿曼达·普拉莫', '蒂姆·罗斯', '塞缪尔·杰克逊', '菲尔·拉马', '布鲁斯·威利斯', '弗兰克·威利', '布尔·斯蒂尔斯', '文·瑞姆斯', '劳拉·拉芙蕾丝', '保罗·考尔德伦...'], 'score': '8.8', 'comment': '(460328人评价)'}, '美丽心灵': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1665997400.jpg', 'movie_name': '美丽心灵', 'other_name': '有你终生美丽(港) / 美丽境界(台)', 'release_time': ['2001-12-13(加州首映)', '2002-01-04(美国)'], 'actor': ['罗素·克劳', '艾德·哈里斯', '詹妮弗·康纳利', '克里斯托弗·普卢默', '保罗·贝坦尼', '亚当·戈德堡', '乔什·卢卡斯', '安东尼·拉普', '贾森·加里-斯坦福德', '贾德·赫希', '奥斯汀·潘德尔顿', '薇薇·卡登尼...'], 'score': '8.9', 'comment': '(411983人评价)'}}


## 3. Xpath 提取


```python
from lxml import etree  # 导入xpath模块
```


```python
xpath_data = etree.HTML(data)  # 初始化xpath结构
```

可以直接在浏览器中试xpath表达式,如下图:  
![xpath1](./images/xpath1.png)  
**下例用到的xpath语法解释:**  
 - "//"  # 代表从根节点搜索
 - "//a"  # 搜索根节点的所有a标签
 - "//a[@class="nbg]"  # 搜索class="nbg"的a标签
 - ".../a"  # 搜索从...节点开始的子a标签
 - ".../img/@src"  # 获取当前img标签的src属性
 - ".../p/text()"  # 获取当前p标签下的文本
 - ".../p//text()"  # 获取当前p标签后的所有文本(子孙文本)


```python
poster = xpath_data.xpath('//a[@class="nbg"]/img/@src')  # 获取海报
movie_name = xpath_data.xpath('//div[@class="pl2"]/a/text()')  # 获取电影名
other_name = xpath_data.xpath('//div[@class="pl2"]/a/span/text()')  # 获取电影别名
time_actor = xpath_data.xpath('//div[@class="pl2"]/p/text()')  # 获取时间和演员
score = xpath_data.xpath('//span[@class="rating_nums"]/text()')  # 获取评分
comment_people = xpath_data.xpath('//span[@class="pl"]/text()')  # 评分人数
movie_data = {}
```

#### 同样进行数据收集


```python
for p, m, o, t, s, c in zip(poster, movie_name, other_name, time_actor, score, comment_people):
    m = m.replace("/", "").strip()
    release_time, actor = get_time_actor(t)
    movie_data.update({m: {"poster": p, "movie_name": m, "other_name": t, "release_time": release_time, "actor": actor, "score": s, "comment": c}})
print(movie_data)
```

    {'辛德勒的名单': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p492406163.jpg', 'movie_name': '辛德勒的名单', 'other_name': '1993-11-30(华盛顿首映) / 1994-02-04(美国) / 连姆·尼森 / 本·金斯利 / 拉尔夫·费因斯 / 卡罗琳·古多尔 / 乔纳森·萨加尔 / 艾伯丝·戴维兹 / 马尔戈萨·格贝尔 / 马克·伊瓦涅 / 碧翠斯·马科拉 / 安德烈·瑟韦林 / 弗里德里希·冯·图恩 / 克齐斯茨托夫·拉夫特...', 'release_time': ['1993-11-30(华盛顿首映)', '1994-02-04(美国)'], 'actor': ['连姆·尼森', '本·金斯利', '拉尔夫·费因斯', '卡罗琳·古多尔', '乔纳森·萨加尔', '艾伯丝·戴维兹', '马尔戈萨·格贝尔', '马克·伊瓦涅', '碧翠斯·马科拉', '安德烈·瑟韦林', '弗里德里希·冯·图恩', '克齐斯茨托夫·拉夫特...'], 'score': '9.5', 'comment': '(571888人评价)'}, '': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1665997400.jpg', 'movie_name': '', 'other_name': '2001-12-13(加州首映) / 2002-01-04(美国) / 罗素·克劳 / 艾德·哈里斯 / 詹妮弗·康纳利 / 克里斯托弗·普卢默 / 保罗·贝坦尼 / 亚当·戈德堡 / 乔什·卢卡斯 / 安东尼·拉普 / 贾森·加里-斯坦福德 / 贾德·赫希 / 奥斯汀·潘德尔顿 / 薇薇·卡登尼...', 'release_time': ['2001-12-13(加州首映)', '2002-01-04(美国)'], 'actor': ['罗素·克劳', '艾德·哈里斯', '詹妮弗·康纳利', '克里斯托弗·普卢默', '保罗·贝坦尼', '亚当·戈德堡', '乔什·卢卡斯', '安东尼·拉普', '贾森·加里-斯坦福德', '贾德·赫希', '奥斯汀·潘德尔顿', '薇薇·卡登尼...'], 'score': '8.9', 'comment': '(411983人评价)'}, '狩猎': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p477229647.jpg', 'movie_name': '狩猎', 'other_name': '1984-02-17(波士顿首映) / 1984-09-28(意大利) / 罗伯特·德尼罗 / 詹姆斯·伍兹 / 伊丽莎白·麦戈文 / 乔·佩西 / 波特·杨 / 塔斯黛·韦尔德 / 特里特·威廉斯 / 丹尼·爱罗 / 理查德·布赖特 / 詹姆斯·海登 / 威廉·弗西斯 / 达兰妮·弗鲁格 / 拉里·拉普...', 'release_time': ['1984-02-17(波士顿首映)', '1984-09-28(意大利)'], 'actor': ['罗伯特·德尼罗', '詹姆斯·伍兹', '伊丽莎白·麦戈文', '乔·佩西', '波特·杨', '塔斯黛·韦尔德', '特里特·威廉斯', '丹尼·爱罗', '理查德·布赖特', '詹姆斯·海登', '威廉·弗西斯', '达兰妮·弗鲁格', '拉里·拉普...'], 'score': '9.1', 'comment': '(232940人评价)'}, '美国往事': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1808872109.jpg', 'movie_name': '美国往事', 'other_name': '2006-03-23(德国) / 乌尔里希·穆埃 / 马蒂娜·格德克 / 塞巴斯蒂安·科赫 / 乌尔里希·图库尔 / 托马斯·蒂梅 / 汉斯-尤韦·鲍尔 / 沃克马·克莱纳特 / 马提亚斯·布伦纳 / 查理·哈纳 / 赫伯特·克瑙普 / 巴斯蒂安·特罗斯特 / 玛丽·格鲁伯...', 'release_time': ['2006-03-23(德国)', '乌尔里希·穆埃'], 'actor': ['马蒂娜·格德克', '塞巴斯蒂安·科赫', '乌尔里希·图库尔', '托马斯·蒂梅', '汉斯-尤韦·鲍尔', '沃克马·克莱纳特', '马提亚斯·布伦纳', '查理·哈纳', '赫伯特·克瑙普', '巴斯蒂安·特罗斯特', '玛丽·格鲁伯...'], 'score': '9.1', 'comment': '(317944人评价)'}, '十二怒汉': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p616779645.jpg', 'movie_name': '十二怒汉', 'other_name': '1972-03-15(纽约首映) / 1972-03-24(美国) / 马龙·白兰度 / 阿尔·帕西诺 / 詹姆斯·肯恩 / 理查德·卡斯特尔诺 / 罗伯特·杜瓦尔 / 斯特林·海登 / 约翰·马利 / 理查德·康特 / 艾尔·勒提埃里 / 黛安·基顿 / 阿贝·维高达 / 塔莉娅·夏尔 / 吉亚尼·罗素...', 'release_time': ['1972-03-15(纽约首映)', '1972-03-24(美国)'], 'actor': ['马龙·白兰度', '阿尔·帕西诺', '詹姆斯·肯恩', '理查德·卡斯特尔诺', '罗伯特·杜瓦尔', '斯特林·海登', '约翰·马利', '理查德·康特', '艾尔·勒提埃里', '黛安·基顿', '阿贝·维高达', '塔莉娅·夏尔', '吉亚尼·罗素...'], 'score': '9.2', 'comment': '(496913人评价)'}, '窃听风暴': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792238287.jpg', 'movie_name': '窃听风暴', 'other_name': '1975-11-19(美国) / 杰克·尼科尔森 / 丹尼·德维托 / 克里斯托弗·洛伊德 / 路易丝·弗莱彻 / 威尔·萨姆森 / 特德·马克兰德 / 布拉德·道里夫 / 斯加特曼·克罗索斯 / 迈克尔·贝里曼 / 彼得·布罗科 / 穆瓦科·卡姆布卡 / 威廉·达尔 / 乔西普·艾利克...', 'release_time': ['1975-11-19(美国)', '杰克·尼科尔森'], 'actor': ['丹尼·德维托', '克里斯托弗·洛伊德', '路易丝·弗莱彻', '威尔·萨姆森', '特德·马克兰德', '布拉德·道里夫', '斯加特曼·克罗索斯', '迈克尔·贝里曼', '彼得·布罗科', '穆瓦科·卡姆布卡', '威廉·达尔', '乔西普·艾利克...'], 'score': '9.1', 'comment': '(354920人评价)'}, '天堂电影院': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792443418.jpg', 'movie_name': '天堂电影院', 'other_name': '1998-08-28(英国) / 杰森·弗莱明 / 德克斯特·弗莱彻 / 尼克·莫兰 / 杰森·斯坦森 / 斯蒂文·麦金托什 / 斯汀 / 维尼·琼斯 / 丹尼·约翰-儒勒 / 维克多·麦奎尔 / 阿兰·福德 / 安德鲁·蒂曼 / 马修·沃恩 / 弗兰克·哈珀 / 罗尼·福克斯 / 罗伯·布莱顿...', 'release_time': ['1998-08-28(英国)', '杰森·弗莱明'], 'actor': ['德克斯特·弗莱彻', '尼克·莫兰', '杰森·斯坦森', '斯蒂文·麦金托什', '斯汀', '维尼·琼斯', '丹尼·约翰-儒勒', '维克多·麦奎尔', '阿兰·福德', '安德鲁·蒂曼', '马修·沃恩', '弗兰克·哈珀', '罗尼·福克斯', '罗伯·布莱顿...'], 'score': '9.1', 'comment': '(352235人评价)'}, '教父': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2513253791.jpg', 'movie_name': '教父', 'other_name': '1994-05-17(戛纳电影节) / 1994-06-30(香港) / 葛优 / 巩俐 / 姜武 / 牛犇 / 郭涛 / 张璐 / 倪大红 / 肖聪 / 董飞 / 刘天池 / 董立范 / 黄宗洛 / 刘燕瑾 / 李连义 / 杨同顺 / 苏岩 / 王丽华 / 中国大陆 / 香港 / 张艺谋 / 132分钟 / 剧情 / 历史 / 家庭...', 'release_time': ['1994-05-17(戛纳电影节)', '1994-06-30(香港)'], 'actor': ['葛优', '巩俐', '姜武', '牛犇', '郭涛', '张璐', '倪大红', '肖聪', '董飞', '刘天池', '董立范', '黄宗洛', '刘燕瑾', '李连义', '杨同顺', '苏岩', '王丽华', '中国大陆', '香港', '张艺谋', '132分钟', '剧情', '历史', '家庭...'], 'score': '9.2', 'comment': '(409160人评价)'}, '一一': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910926158.jpg', 'movie_name': '一一', 'other_name': '1999-09-10(威尼斯电影节) / 1999-10-15(美国) / 爱德华·诺顿 / 布拉德·皮特 / 海伦娜·伯翰·卡特 / 扎克·格雷尼尔 / 米特·洛夫 / 杰瑞德·莱托 / 艾恩·贝利 / 里奇蒙德·阿奎特  / 乔治·马奎尔 / 鲍勃·斯蒂芬森 / Carl Ciarfalio / 斯图尔特·布拉姆博格...', 'release_time': ['1999-09-10(威尼斯电影节)', '1999-10-15(美国)'], 'actor': ['爱德华·诺顿', '布拉德·皮特', '海伦娜·伯翰·卡特', '扎克·格雷尼尔', '米特·洛夫', '杰瑞德·莱托', '艾恩·贝利', '里奇蒙德·阿奎特 ', '乔治·马奎尔', '鲍勃·斯蒂芬森', 'Carl Ciarfalio', '斯图尔特·布拉姆博格...'], 'score': '9.0', 'comment': '(514373人评价)'}, '飞越疯人院': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1465235231.jpg', 'movie_name': '飞越疯人院', 'other_name': '2005-12-11(BNAT电影节) / 2006-03-17(美国) / 娜塔莉·波特曼 / 雨果·维文 / 斯蒂芬·瑞 / 斯蒂芬·弗雷 / 约翰·赫特 / 蒂姆·皮戈特-史密斯 / 鲁珀特·格雷夫斯 / 罗杰·阿拉姆 / 本·迈尔斯 / 西妮德·库萨克 / 娜塔莎·怀特曼 / 约翰·斯坦丁 /...', 'release_time': ['2005-12-11(BNAT电影节)', '2006-03-17(美国)'], 'actor': ['娜塔莉·波特曼', '雨果·维文', '斯蒂芬·瑞', '斯蒂芬·弗雷', '约翰·赫特', '蒂姆·皮戈特-史密斯', '鲁珀特·格雷夫斯', '罗杰·阿拉姆', '本·迈尔斯', '西妮德·库萨克', '娜塔莎·怀特曼', '约翰·斯坦丁 /...'], 'score': '8.8', 'comment': '(593760人评价)'}, '鬼子来了': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910902213.jpg', 'movie_name': '鬼子来了', 'other_name': '1994-05-12(戛纳电影节) / 1994-10-14(美国) / 约翰·特拉沃尔塔 / 乌玛·瑟曼 / 阿曼达·普拉莫 / 蒂姆·罗斯 / 塞缪尔·杰克逊 / 菲尔·拉马 / 布鲁斯·威利斯 / 弗兰克·威利 / 布尔·斯蒂尔斯 / 文·瑞姆斯 / 劳拉·拉芙蕾丝 / 保罗·考尔德伦...', 'release_time': ['1994-05-12(戛纳电影节)', '1994-10-14(美国)'], 'actor': ['约翰·特拉沃尔塔', '乌玛·瑟曼', '阿曼达·普拉莫', '蒂姆·罗斯', '塞缪尔·杰克逊', '菲尔·拉马', '布鲁斯·威利斯', '弗兰克·威利', '布尔·斯蒂尔斯', '文·瑞姆斯', '劳拉·拉芙蕾丝', '保罗·考尔德伦...'], 'score': '8.8', 'comment': '(460328人评价)'}}


## 4. Pyquery 的数据提取
主要利用jquery的定位方式，  
如 ".name" 表示 class="name"   
"#name" 表示 id="name"  
以下例子中:
  - "a.nbg"  # 表示 a class="nbg"
  - "a img"  # 表示 a标签的子孙img标签
  - .remove()  # 表示移除该节点
  - .items()  # 当选中多个节点时,需要使用.items() 生成可遍历对象再进行提取
  - .attr()  # 表示获取标签
  - .text()  # 表示获取文本


```python
from pyquery import PyQuery as pq
```


```python
query_data = pq(data[:])  # 因为为了便于提取,需要删除节点,避免破坏元数据,拷贝一份
```


```python
poster = (i.attr["src"] for i in query_data("a.nbg img").items())  # 获取海报
other_name = [i.text() for i in query_data("div.pl2 a span").items()]  # 获取别名
query_data("div.pl2 a span").remove()  # 移除别名节点
movie_name = (i.text().strip("/").strip() for i in query_data("div.pl2 a").items())  # 获取电影名
time_actor =  (i.text() for i in query_data("div.pl2 p").items())  # 获取上映时间和演员
score = (i.text() for i in query_data("span.rating_nums").items())  # 获取评分
comment_people = (i.text() for i in query_data("span.pl").items())  # 获取评价人数
movie_data = {}
```


```python
for p, m, o, t, s, c in zip(poster, movie_name, other_name, time_actor, score, comment_people):
    release_time, actor = get_time_actor(t)
    movie_data.update({m: {"poster": p, "movie_name": m, "other_name": t, "release_time": release_time, "actor": actor, "score": s, "comment": c}})
print(movie_data)
```

    {'辛德勒的名单': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p492406163.jpg', 'movie_name': '辛德勒的名单', 'other_name': '1993-11-30(华盛顿首映) / 1994-02-04(美国) / 连姆·尼森 / 本·金斯利 / 拉尔夫·费因斯 / 卡罗琳·古多尔 / 乔纳森·萨加尔 / 艾伯丝·戴维兹 / 马尔戈萨·格贝尔 / 马克·伊瓦涅 / 碧翠斯·马科拉 / 安德烈·瑟韦林 / 弗里德里希·冯·图恩 / 克齐斯茨托夫·拉夫特...', 'release_time': ['1993-11-30(华盛顿首映)', '1994-02-04(美国)'], 'actor': ['连姆·尼森', '本·金斯利', '拉尔夫·费因斯', '卡罗琳·古多尔', '乔纳森·萨加尔', '艾伯丝·戴维兹', '马尔戈萨·格贝尔', '马克·伊瓦涅', '碧翠斯·马科拉', '安德烈·瑟韦林', '弗里德里希·冯·图恩', '克齐斯茨托夫·拉夫特...'], 'score': '9.5', 'comment': '(571888人评价)'}, '狩猎': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1546987967.jpg', 'movie_name': '狩猎', 'other_name': '2012-05-20(戛纳电影节) / 2013-01-10(丹麦) / 麦斯·米科尔森 / 托玛斯·博·拉森 / 安妮卡·韦德科普 / 拉丝·弗格斯托姆 / 苏西·沃德 / 安妮·路易丝·哈辛 / 拉斯·兰特 / 亚历山德拉·拉帕波特 / 拉斯穆斯·林德·鲁宾 / 丹麦 / 瑞典 / 托马斯·温特伯格...', 'release_time': ['2012-05-20(戛纳电影节)', '2013-01-10(丹麦)'], 'actor': ['麦斯·米科尔森', '托玛斯·博·拉森', '安妮卡·韦德科普', '拉丝·弗格斯托姆', '苏西·沃德', '安妮·路易丝·哈辛', '拉斯·兰特', '亚历山德拉·拉帕波特', '拉斯穆斯·林德·鲁宾', '丹麦', '瑞典', '托马斯·温特伯格...'], 'score': '9.1', 'comment': '(184560人评价)'}, '美国往事': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p477229647.jpg', 'movie_name': '美国往事', 'other_name': '1984-02-17(波士顿首映) / 1984-09-28(意大利) / 罗伯特·德尼罗 / 詹姆斯·伍兹 / 伊丽莎白·麦戈文 / 乔·佩西 / 波特·杨 / 塔斯黛·韦尔德 / 特里特·威廉斯 / 丹尼·爱罗 / 理查德·布赖特 / 詹姆斯·海登 / 威廉·弗西斯 / 达兰妮·弗鲁格 / 拉里·拉普...', 'release_time': ['1984-02-17(波士顿首映)', '1984-09-28(意大利)'], 'actor': ['罗伯特·德尼罗', '詹姆斯·伍兹', '伊丽莎白·麦戈文', '乔·佩西', '波特·杨', '塔斯黛·韦尔德', '特里特·威廉斯', '丹尼·爱罗', '理查德·布赖特', '詹姆斯·海登', '威廉·弗西斯', '达兰妮·弗鲁格', '拉里·拉普...'], 'score': '9.1', 'comment': '(232940人评价)'}, '十二怒汉': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2173577632.jpg', 'movie_name': '十二怒汉', 'other_name': '1957-04-13(美国) / 亨利·方达 / 马丁·鲍尔萨姆 / 约翰·菲德勒 / 李·科布 / E.G.马绍尔 / 杰克·克卢格曼 / 爱德华·宾斯 / 杰克·瓦尔登 / 约瑟夫·史威尼 / 埃德·贝格利 / 乔治·沃斯科维奇 / 罗伯特·韦伯 / 美国 / 西德尼·吕美特 / 96 分钟...', 'release_time': ['1957-04-13(美国)', '亨利·方达'], 'actor': ['马丁·鲍尔萨姆', '约翰·菲德勒', '李·科布', 'E.G.马绍尔', '杰克·克卢格曼', '爱德华·宾斯', '杰克·瓦尔登', '约瑟夫·史威尼', '埃德·贝格利', '乔治·沃斯科维奇', '罗伯特·韦伯', '美国', '西德尼·吕美特', '96 分钟...'], 'score': '9.4', 'comment': '(238341人评价)'}, '窃听风暴': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1808872109.jpg', 'movie_name': '窃听风暴', 'other_name': '2006-03-23(德国) / 乌尔里希·穆埃 / 马蒂娜·格德克 / 塞巴斯蒂安·科赫 / 乌尔里希·图库尔 / 托马斯·蒂梅 / 汉斯-尤韦·鲍尔 / 沃克马·克莱纳特 / 马提亚斯·布伦纳 / 查理·哈纳 / 赫伯特·克瑙普 / 巴斯蒂安·特罗斯特 / 玛丽·格鲁伯...', 'release_time': ['2006-03-23(德国)', '乌尔里希·穆埃'], 'actor': ['马蒂娜·格德克', '塞巴斯蒂安·科赫', '乌尔里希·图库尔', '托马斯·蒂梅', '汉斯-尤韦·鲍尔', '沃克马·克莱纳特', '马提亚斯·布伦纳', '查理·哈纳', '赫伯特·克瑙普', '巴斯蒂安·特罗斯特', '玛丽·格鲁伯...'], 'score': '9.1', 'comment': '(317944人评价)'}, '天堂电影院': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910901025.jpg', 'movie_name': '天堂电影院', 'other_name': '1988-11-17(意大利) / 安东内拉·阿蒂利 / 恩佐·卡拉瓦勒 / 艾萨·丹尼埃利 / 里奥·故罗塔 / 马克·莱昂纳蒂 / 普佩拉·玛奇奥 / 阿格妮丝·那诺 / 莱奥波多·特里耶斯泰 / 萨瓦特利·卡西欧 / 尼古拉·迪·平托 / 罗伯塔·蕾娜 / 尼诺·戴罗佐...', 'release_time': ['1988-11-17(意大利)', '安东内拉·阿蒂利'], 'actor': ['恩佐·卡拉瓦勒', '艾萨·丹尼埃利', '里奥·故罗塔', '马克·莱昂纳蒂', '普佩拉·玛奇奥', '阿格妮丝·那诺', '莱奥波多·特里耶斯泰', '萨瓦特利·卡西欧', '尼古拉·迪·平托', '罗伯塔·蕾娜', '尼诺·戴罗佐...'], 'score': '9.2', 'comment': '(396652人评价)'}, '教父': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p616779645.jpg', 'movie_name': '教父', 'other_name': '1972-03-15(纽约首映) / 1972-03-24(美国) / 马龙·白兰度 / 阿尔·帕西诺 / 詹姆斯·肯恩 / 理查德·卡斯特尔诺 / 罗伯特·杜瓦尔 / 斯特林·海登 / 约翰·马利 / 理查德·康特 / 艾尔·勒提埃里 / 黛安·基顿 / 阿贝·维高达 / 塔莉娅·夏尔 / 吉亚尼·罗素...', 'release_time': ['1972-03-15(纽约首映)', '1972-03-24(美国)'], 'actor': ['马龙·白兰度', '阿尔·帕西诺', '詹姆斯·肯恩', '理查德·卡斯特尔诺', '罗伯特·杜瓦尔', '斯特林·海登', '约翰·马利', '理查德·康特', '艾尔·勒提埃里', '黛安·基顿', '阿贝·维高达', '塔莉娅·夏尔', '吉亚尼·罗素...'], 'score': '9.2', 'comment': '(496913人评价)'}, '一一': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2119675128.jpg', 'movie_name': '一一', 'other_name': '2000-05-14(戛纳电影节) / 2000-12-16(日本) / 2017-07-28(台湾) / 李凯莉 / 金燕玲 / 张洋洋 / 萧淑慎 / 尾形一成 / 陈希圣 / 林孟瑾 / 陈以文 / 柯宇纶 / 柯素云 / 唐如韫 / 徐淑媛 / 陶传正 / 孙法钧 / 津田健次郎 / 江惠惠 / 李永丰 / 许安安 / 戴立忍...', 'release_time': ['2000-05-14(戛纳电影节)', '2000-12-16(日本)'], 'actor': ['2017-07-28(台湾)', '李凯莉', '金燕玲', '张洋洋', '萧淑慎', '尾形一成', '陈希圣', '林孟瑾', '陈以文', '柯宇纶', '柯素云', '唐如韫', '徐淑媛', '陶传正', '孙法钧', '津田健次郎', '江惠惠', '李永丰', '许安安', '戴立忍...'], 'score': '9.0', 'comment': '(199330人评价)'}, '飞越疯人院': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792238287.jpg', 'movie_name': '飞越疯人院', 'other_name': '1975-11-19(美国) / 杰克·尼科尔森 / 丹尼·德维托 / 克里斯托弗·洛伊德 / 路易丝·弗莱彻 / 威尔·萨姆森 / 特德·马克兰德 / 布拉德·道里夫 / 斯加特曼·克罗索斯 / 迈克尔·贝里曼 / 彼得·布罗科 / 穆瓦科·卡姆布卡 / 威廉·达尔 / 乔西普·艾利克...', 'release_time': ['1975-11-19(美国)', '杰克·尼科尔森'], 'actor': ['丹尼·德维托', '克里斯托弗·洛伊德', '路易丝·弗莱彻', '威尔·萨姆森', '特德·马克兰德', '布拉德·道里夫', '斯加特曼·克罗索斯', '迈克尔·贝里曼', '彼得·布罗科', '穆瓦科·卡姆布卡', '威廉·达尔', '乔西普·艾利克...'], 'score': '9.1', 'comment': '(354920人评价)'}, '鬼子来了': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1181775734.jpg', 'movie_name': '鬼子来了', 'other_name': '2000-05-12(戛纳电影节) / 2002-04-27(日本) / 姜文 / 香川照之 / 袁丁 / 姜宏波 / 丛志军 / 喜子 / 泽田谦也 / 李海滨 / 蔡卫东 / 陈述 / 陈莲梅 / 史建全 / 陈强 / 宫路佳具 / 吴大维 / 梶冈润一 / 石山雄大 / 述平 / 姜武 / 中国大陆 / 姜文 / 139分钟...', 'release_time': ['2000-05-12(戛纳电影节)', '2002-04-27(日本)'], 'actor': ['姜文', '香川照之', '袁丁', '姜宏波', '丛志军', '喜子', '泽田谦也', '李海滨', '蔡卫东', '陈述', '陈莲梅', '史建全', '陈强', '宫路佳具', '吴大维', '梶冈润一', '石山雄大', '述平', '姜武', '中国大陆', '姜文', '139分钟...'], 'score': '9.2', 'comment': '(334681人评价)'}, '两杆大烟枪': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792443418.jpg', 'movie_name': '两杆大烟枪', 'other_name': '1998-08-28(英国) / 杰森·弗莱明 / 德克斯特·弗莱彻 / 尼克·莫兰 / 杰森·斯坦森 / 斯蒂文·麦金托什 / 斯汀 / 维尼·琼斯 / 丹尼·约翰-儒勒 / 维克多·麦奎尔 / 阿兰·福德 / 安德鲁·蒂曼 / 马修·沃恩 / 弗兰克·哈珀 / 罗尼·福克斯 / 罗伯·布莱顿...', 'release_time': ['1998-08-28(英国)', '杰森·弗莱明'], 'actor': ['德克斯特·弗莱彻', '尼克·莫兰', '杰森·斯坦森', '斯蒂文·麦金托什', '斯汀', '维尼·琼斯', '丹尼·约翰-儒勒', '维克多·麦奎尔', '阿兰·福德', '安德鲁·蒂曼', '马修·沃恩', '弗兰克·哈珀', '罗尼·福克斯', '罗伯·布莱顿...'], 'score': '9.1', 'comment': '(352235人评价)'}, '被嫌弃的松子的一生': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p453723669.jpg', 'movie_name': '被嫌弃的松子的一生', 'other_name': '2006-05-27(日本) / 中谷美纪 / 瑛太 / 香川照之 / 市川实日子 / 伊势谷友介 / 柄本明 / 黑泽明日香 / 荒川良良 / 柴崎幸 / 土屋安娜 / 奥之矢佳奈 / 谷原章介 / 武田真治 / 片平渚 / 宫藤官九郎 / 角野卓造 / 田中要次 / 木村凯拉 / 谷中敦...', 'release_time': ['2006-05-27(日本)', '中谷美纪'], 'actor': ['瑛太', '香川照之', '市川实日子', '伊势谷友介', '柄本明', '黑泽明日香', '荒川良良', '柴崎幸', '土屋安娜', '奥之矢佳奈', '谷原章介', '武田真治', '片平渚', '宫藤官九郎', '角野卓造', '田中要次', '木村凯拉', '谷中敦...'], 'score': '8.9', 'comment': '(414122人评价)'}, '活着': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2513253791.jpg', 'movie_name': '活着', 'other_name': '1994-05-17(戛纳电影节) / 1994-06-30(香港) / 葛优 / 巩俐 / 姜武 / 牛犇 / 郭涛 / 张璐 / 倪大红 / 肖聪 / 董飞 / 刘天池 / 董立范 / 黄宗洛 / 刘燕瑾 / 李连义 / 杨同顺 / 苏岩 / 王丽华 / 中国大陆 / 香港 / 张艺谋 / 132分钟 / 剧情 / 历史 / 家庭...', 'release_time': ['1994-05-17(戛纳电影节)', '1994-06-30(香港)'], 'actor': ['葛优', '巩俐', '姜武', '牛犇', '郭涛', '张璐', '倪大红', '肖聪', '董飞', '刘天池', '董立范', '黄宗洛', '刘燕瑾', '李连义', '杨同顺', '苏岩', '王丽华', '中国大陆', '香港', '张艺谋', '132分钟', '剧情', '历史', '家庭...'], 'score': '9.2', 'comment': '(409160人评价)'}, '楚门的世界': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg', 'movie_name': '楚门的世界', 'other_name': '1998-06-05(美国) / 金·凯瑞 / 劳拉·琳妮 / 艾德·哈里斯 / 诺亚·艾默里奇 / 娜塔莎·麦克艾霍恩 / 马西娅·德波尼斯 / Adam Tomei / 哈里·谢尔 / 约翰·普莱舍 / 澳澜·琼斯 / Joe Minjares / 特里·金瑞利 / 乔尔·麦金农·米勒 / 冈本玉二 / Jake Eberle...', 'release_time': ['1998-06-05(美国)', '金·凯瑞'], 'actor': ['劳拉·琳妮', '艾德·哈里斯', '诺亚·艾默里奇', '娜塔莎·麦克艾霍恩', '马西娅·德波尼斯', 'Adam Tomei', '哈里·谢尔', '约翰·普莱舍', '澳澜·琼斯', 'Joe Minjares', '特里·金瑞利', '乔尔·麦金农·米勒', '冈本玉二', 'Jake Eberle...'], 'score': '9.2', 'comment': '(755718人评价)'}, '搏击俱乐部': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910926158.jpg', 'movie_name': '搏击俱乐部', 'other_name': '1999-09-10(威尼斯电影节) / 1999-10-15(美国) / 爱德华·诺顿 / 布拉德·皮特 / 海伦娜·伯翰·卡特 / 扎克·格雷尼尔 / 米特·洛夫 / 杰瑞德·莱托 / 艾恩·贝利 / 里奇蒙德·阿奎特 / 乔治·马奎尔 / 鲍勃·斯蒂芬森 / Carl Ciarfalio / 斯图尔特·布拉姆博格...', 'release_time': ['1999-09-10(威尼斯电影节)', '1999-10-15(美国)'], 'actor': ['爱德华·诺顿', '布拉德·皮特', '海伦娜·伯翰·卡特', '扎克·格雷尼尔', '米特·洛夫', '杰瑞德·莱托', '艾恩·贝利', '里奇蒙德·阿奎特', '乔治·马奎尔', '鲍勃·斯蒂芬森', 'Carl Ciarfalio', '斯图尔特·布拉姆博格...'], 'score': '9.0', 'comment': '(514373人评价)'}, '死亡诗社': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910824340.jpg', 'movie_name': '死亡诗社', 'other_name': '1989-06-02(多伦多首映) / 1989-06-09(美国) / 罗宾·威廉姆斯 / 罗伯特·肖恩·莱纳德 / 伊桑·霍克 / 乔西·查尔斯 / 盖尔·汉森 / 迪伦·库斯曼 / 阿勒隆·鲁杰罗 / 詹姆斯·沃特斯顿 / 诺曼·劳埃德 / 柯特伍德·史密斯 / 卡拉·贝尔韦尔 / 利昂·波纳尔...', 'release_time': ['1989-06-02(多伦多首映)', '1989-06-09(美国)'], 'actor': ['罗宾·威廉姆斯', '罗伯特·肖恩·莱纳德', '伊桑·霍克', '乔西·查尔斯', '盖尔·汉森', '迪伦·库斯曼', '阿勒隆·鲁杰罗', '詹姆斯·沃特斯顿', '诺曼·劳埃德', '柯特伍德·史密斯', '卡拉·贝尔韦尔', '利昂·波纳尔...'], 'score': '9.0', 'comment': '(388695人评价)'}, 'V字仇杀队': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1465235231.jpg', 'movie_name': 'V字仇杀队', 'other_name': '2005-12-11(BNAT电影节) / 2006-03-17(美国) / 娜塔莉·波特曼 / 雨果·维文 / 斯蒂芬·瑞 / 斯蒂芬·弗雷 / 约翰·赫特 / 蒂姆·皮戈特-史密斯 / 鲁珀特·格雷夫斯 / 罗杰·阿拉姆 / 本·迈尔斯 / 西妮德·库萨克 / 娜塔莎·怀特曼 / 约翰·斯坦丁 /...', 'release_time': ['2005-12-11(BNAT电影节)', '2006-03-17(美国)'], 'actor': ['娜塔莉·波特曼', '雨果·维文', '斯蒂芬·瑞', '斯蒂芬·弗雷', '约翰·赫特', '蒂姆·皮戈特-史密斯', '鲁珀特·格雷夫斯', '罗杰·阿拉姆', '本·迈尔斯', '西妮德·库萨克', '娜塔莎·怀特曼', '约翰·斯坦丁 /...'], 'score': '8.8', 'comment': '(593760人评价)'}, '闻香识女人': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2550757929.jpg', 'movie_name': '闻香识女人', 'other_name': '1992-12-23(美国) / 阿尔·帕西诺 / 克里斯·奥唐纳 / 詹姆斯·瑞布霍恩 / 加布里埃尔·安瓦尔 / 菲利普·塞默·霍夫曼 / 理查德·文彻 / 布莱德利·惠特福德 / 罗谢尔·奥利弗 / 托德·路易斯 / 马特·史密斯 / 吉恩·坎菲尔德 / 弗兰西丝·康罗伊...', 'release_time': ['1992-12-23(美国)', '阿尔·帕西诺'], 'actor': ['克里斯·奥唐纳', '詹姆斯·瑞布霍恩', '加布里埃尔·安瓦尔', '菲利普·塞默·霍夫曼', '理查德·文彻', '布莱德利·惠特福德', '罗谢尔·奥利弗', '托德·路易斯', '马特·史密斯', '吉恩·坎菲尔德', '弗兰西丝·康罗伊...'], 'score': '9.0', 'comment': '(457858人评价)'}, '低俗小说': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910902213.jpg', 'movie_name': '低俗小说', 'other_name': '1994-05-12(戛纳电影节) / 1994-10-14(美国) / 约翰·特拉沃尔塔 / 乌玛·瑟曼 / 阿曼达·普拉莫 / 蒂姆·罗斯 / 塞缪尔·杰克逊 / 菲尔·拉马 / 布鲁斯·威利斯 / 弗兰克·威利 / 布尔·斯蒂尔斯 / 文·瑞姆斯 / 劳拉·拉芙蕾丝 / 保罗·考尔德伦...', 'release_time': ['1994-05-12(戛纳电影节)', '1994-10-14(美国)'], 'actor': ['约翰·特拉沃尔塔', '乌玛·瑟曼', '阿曼达·普拉莫', '蒂姆·罗斯', '塞缪尔·杰克逊', '菲尔·拉马', '布鲁斯·威利斯', '弗兰克·威利', '布尔·斯蒂尔斯', '文·瑞姆斯', '劳拉·拉芙蕾丝', '保罗·考尔德伦...'], 'score': '8.8', 'comment': '(460328人评价)'}, '美丽心灵': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1665997400.jpg', 'movie_name': '美丽心灵', 'other_name': '2001-12-13(加州首映) / 2002-01-04(美国) / 罗素·克劳 / 艾德·哈里斯 / 詹妮弗·康纳利 / 克里斯托弗·普卢默 / 保罗·贝坦尼 / 亚当·戈德堡 / 乔什·卢卡斯 / 安东尼·拉普 / 贾森·加里-斯坦福德 / 贾德·赫希 / 奥斯汀·潘德尔顿 / 薇薇·卡登尼...', 'release_time': ['2001-12-13(加州首映)', '2002-01-04(美国)'], 'actor': ['罗素·克劳', '艾德·哈里斯', '詹妮弗·康纳利', '克里斯托弗·普卢默', '保罗·贝坦尼', '亚当·戈德堡', '乔什·卢卡斯', '安东尼·拉普', '贾森·加里-斯坦福德', '贾德·赫希', '奥斯汀·潘德尔顿', '薇薇·卡登尼...'], 'score': '8.9', 'comment': '(411983人评价)'}}


## 5. scrapy 混合提取


```python
from scrapy import Selector  # 导入scrapy的选择器
```


```python
se = Selector(text=data)
```

#### 提取规则说明 从下方案例可以看出,scrapy的提取器,css和xpath,以及正则提取都是支持的,我们可以混用  
   - .css()  # 就是css规则的提取
   - .xpath()  # 就是xpath规则的提取,需要注意的是,因为scrapy的Selector支持混用,如果xpath是在某个提取器之后,那么必须使用"./"来跟进上个提取器的提取点,不能使用"//", 因为Selector 的xapth提取器的"//"永远代表根节点
       - response.css("#id").xpath("./a")  # 该规则表示id="id" 的节点**之后**的所有a标签节点
       - response.css("#id").xpath("//a")  # 改规则就变成了提取所有的a标签节点,前面的css选择器的结果失效.
   - .re()  # 就是正则的提取, 正则提取后,不需要用extract()来转化成str类型
   - extract()  # 将当前的选择结果转化成str类型  


```python
poster = se.css(".nbg img").xpath("./@src").extract()  # 获取海报
movie_name = se.css("div.pl2").xpath("./a/text()").re("\w+")  # 获取电影名
other_name = se.css("div.pl2").xpath("./a/span/text()").extract()  # 获取电影别名
time_actor = se.css("div.pl2").xpath("./p/text()").extract()  # 获取上映日期和演员
score = se.css("span.rating_nums::text").extract()  # 获取评分
comment_people = se.xpath('//span[@class="pl"]/text()').extract()  # 获取评分人数
movie_data = {}
```


```python
for p, m, o, t, s, c in zip(poster, movie_name, other_name, time_actor, score, comment_people):
    release_time, actor = get_time_actor(t)
    movie_data.update({m: {"poster": p, "movie_name": m, "other_name": t, "release_time": release_time, "actor": actor, "score": s, "comment": c}})
print(movie_data)
```

    {'辛德勒的名单': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p492406163.jpg', 'movie_name': '辛德勒的名单', 'other_name': '1993-11-30(华盛顿首映) / 1994-02-04(美国) / 连姆·尼森 / 本·金斯利 / 拉尔夫·费因斯 / 卡罗琳·古多尔 / 乔纳森·萨加尔 / 艾伯丝·戴维兹 / 马尔戈萨·格贝尔 / 马克·伊瓦涅 / 碧翠斯·马科拉 / 安德烈·瑟韦林 / 弗里德里希·冯·图恩 / 克齐斯茨托夫·拉夫特...', 'release_time': ['1993-11-30(华盛顿首映)', '1994-02-04(美国)'], 'actor': ['连姆·尼森', '本·金斯利', '拉尔夫·费因斯', '卡罗琳·古多尔', '乔纳森·萨加尔', '艾伯丝·戴维兹', '马尔戈萨·格贝尔', '马克·伊瓦涅', '碧翠斯·马科拉', '安德烈·瑟韦林', '弗里德里希·冯·图恩', '克齐斯茨托夫·拉夫特...'], 'score': '9.5', 'comment': '(571888人评价)'}, '狩猎': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1546987967.jpg', 'movie_name': '狩猎', 'other_name': '2012-05-20(戛纳电影节) / 2013-01-10(丹麦) / 麦斯·米科尔森 / 托玛斯·博·拉森 / 安妮卡·韦德科普 / 拉丝·弗格斯托姆 / 苏西·沃德 / 安妮·路易丝·哈辛 / 拉斯·兰特 / 亚历山德拉·拉帕波特 / 拉斯穆斯·林德·鲁宾 / 丹麦 / 瑞典 / 托马斯·温特伯格...', 'release_time': ['2012-05-20(戛纳电影节)', '2013-01-10(丹麦)'], 'actor': ['麦斯·米科尔森', '托玛斯·博·拉森', '安妮卡·韦德科普', '拉丝·弗格斯托姆', '苏西·沃德', '安妮·路易丝·哈辛', '拉斯·兰特', '亚历山德拉·拉帕波特', '拉斯穆斯·林德·鲁宾', '丹麦', '瑞典', '托马斯·温特伯格...'], 'score': '9.1', 'comment': '(184560人评价)'}, '美国往事': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p477229647.jpg', 'movie_name': '美国往事', 'other_name': '1984-02-17(波士顿首映) / 1984-09-28(意大利) / 罗伯特·德尼罗 / 詹姆斯·伍兹 / 伊丽莎白·麦戈文 / 乔·佩西 / 波特·杨 / 塔斯黛·韦尔德 / 特里特·威廉斯 / 丹尼·爱罗 / 理查德·布赖特 / 詹姆斯·海登 / 威廉·弗西斯 / 达兰妮·弗鲁格 / 拉里·拉普...', 'release_time': ['1984-02-17(波士顿首映)', '1984-09-28(意大利)'], 'actor': ['罗伯特·德尼罗', '詹姆斯·伍兹', '伊丽莎白·麦戈文', '乔·佩西', '波特·杨', '塔斯黛·韦尔德', '特里特·威廉斯', '丹尼·爱罗', '理查德·布赖特', '詹姆斯·海登', '威廉·弗西斯', '达兰妮·弗鲁格', '拉里·拉普...'], 'score': '9.1', 'comment': '(232940人评价)'}, '十二怒汉': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2173577632.jpg', 'movie_name': '十二怒汉', 'other_name': '1957-04-13(美国) / 亨利·方达 / 马丁·鲍尔萨姆 / 约翰·菲德勒 / 李·科布 / E.G.马绍尔 / 杰克·克卢格曼  / 爱德华·宾斯 / 杰克·瓦尔登 / 约瑟夫·史威尼 / 埃德·贝格利 / 乔治·沃斯科维奇 / 罗伯特·韦伯 / 美国 / 西德尼·吕美特 / 96 分钟...', 'release_time': ['1957-04-13(美国)', '亨利·方达'], 'actor': ['马丁·鲍尔萨姆', '约翰·菲德勒', '李·科布', 'E.G.马绍尔', '杰克·克卢格曼 ', '爱德华·宾斯', '杰克·瓦尔登', '约瑟夫·史威尼', '埃德·贝格利', '乔治·沃斯科维奇', '罗伯特·韦伯', '美国', '西德尼·吕美特', '96 分钟...'], 'score': '9.4', 'comment': '(238341人评价)'}, '窃听风暴': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1808872109.jpg', 'movie_name': '窃听风暴', 'other_name': '2006-03-23(德国) / 乌尔里希·穆埃 / 马蒂娜·格德克 / 塞巴斯蒂安·科赫 / 乌尔里希·图库尔 / 托马斯·蒂梅 / 汉斯-尤韦·鲍尔 / 沃克马·克莱纳特 / 马提亚斯·布伦纳 / 查理·哈纳 / 赫伯特·克瑙普 / 巴斯蒂安·特罗斯特 / 玛丽·格鲁伯...', 'release_time': ['2006-03-23(德国)', '乌尔里希·穆埃'], 'actor': ['马蒂娜·格德克', '塞巴斯蒂安·科赫', '乌尔里希·图库尔', '托马斯·蒂梅', '汉斯-尤韦·鲍尔', '沃克马·克莱纳特', '马提亚斯·布伦纳', '查理·哈纳', '赫伯特·克瑙普', '巴斯蒂安·特罗斯特', '玛丽·格鲁伯...'], 'score': '9.1', 'comment': '(317944人评价)'}, '天堂电影院': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910901025.jpg', 'movie_name': '天堂电影院', 'other_name': '1988-11-17(意大利) / 安东内拉·阿蒂利 / 恩佐·卡拉瓦勒 / 艾萨·丹尼埃利 / 里奥·故罗塔 / 马克·莱昂纳蒂 / 普佩拉·玛奇奥 / 阿格妮丝·那诺 / 莱奥波多·特里耶斯泰 / 萨瓦特利·卡西欧 / 尼古拉·迪·平托 / 罗伯塔·蕾娜 / 尼诺·戴罗佐...', 'release_time': ['1988-11-17(意大利)', '安东内拉·阿蒂利'], 'actor': ['恩佐·卡拉瓦勒', '艾萨·丹尼埃利', '里奥·故罗塔', '马克·莱昂纳蒂', '普佩拉·玛奇奥', '阿格妮丝·那诺', '莱奥波多·特里耶斯泰', '萨瓦特利·卡西欧', '尼古拉·迪·平托', '罗伯塔·蕾娜', '尼诺·戴罗佐...'], 'score': '9.2', 'comment': '(396652人评价)'}, '教父': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p616779645.jpg', 'movie_name': '教父', 'other_name': '1972-03-15(纽约首映) / 1972-03-24(美国) / 马龙·白兰度 / 阿尔·帕西诺 / 詹姆斯·肯恩 / 理查德·卡斯特尔诺 / 罗伯特·杜瓦尔 / 斯特林·海登 / 约翰·马利 / 理查德·康特 / 艾尔·勒提埃里 / 黛安·基顿 / 阿贝·维高达 / 塔莉娅·夏尔 / 吉亚尼·罗素...', 'release_time': ['1972-03-15(纽约首映)', '1972-03-24(美国)'], 'actor': ['马龙·白兰度', '阿尔·帕西诺', '詹姆斯·肯恩', '理查德·卡斯特尔诺', '罗伯特·杜瓦尔', '斯特林·海登', '约翰·马利', '理查德·康特', '艾尔·勒提埃里', '黛安·基顿', '阿贝·维高达', '塔莉娅·夏尔', '吉亚尼·罗素...'], 'score': '9.2', 'comment': '(496913人评价)'}, '一一': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2119675128.jpg', 'movie_name': '一一', 'other_name': '2000-05-14(戛纳电影节) / 2000-12-16(日本) / 2017-07-28(台湾) / 李凯莉 / 金燕玲 / 张洋洋 / 萧淑慎 / 尾形一成 / 陈希圣 / 林孟瑾 / 陈以文 / 柯宇纶 / 柯素云 / 唐如韫 / 徐淑媛 / 陶传正 / 孙法钧 / 津田健次郎 / 江惠惠 / 李永丰 / 许安安 / 戴立忍...', 'release_time': ['2000-05-14(戛纳电影节)', '2000-12-16(日本)'], 'actor': ['2017-07-28(台湾)', '李凯莉', '金燕玲', '张洋洋', '萧淑慎', '尾形一成', '陈希圣', '林孟瑾', '陈以文', '柯宇纶', '柯素云', '唐如韫', '徐淑媛', '陶传正', '孙法钧', '津田健次郎', '江惠惠', '李永丰', '许安安', '戴立忍...'], 'score': '9.0', 'comment': '(199330人评价)'}, '飞越疯人院': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792238287.jpg', 'movie_name': '飞越疯人院', 'other_name': '1975-11-19(美国) / 杰克·尼科尔森 / 丹尼·德维托 / 克里斯托弗·洛伊德 / 路易丝·弗莱彻 / 威尔·萨姆森 / 特德·马克兰德 / 布拉德·道里夫 / 斯加特曼·克罗索斯 / 迈克尔·贝里曼 / 彼得·布罗科 / 穆瓦科·卡姆布卡 / 威廉·达尔 / 乔西普·艾利克...', 'release_time': ['1975-11-19(美国)', '杰克·尼科尔森'], 'actor': ['丹尼·德维托', '克里斯托弗·洛伊德', '路易丝·弗莱彻', '威尔·萨姆森', '特德·马克兰德', '布拉德·道里夫', '斯加特曼·克罗索斯', '迈克尔·贝里曼', '彼得·布罗科', '穆瓦科·卡姆布卡', '威廉·达尔', '乔西普·艾利克...'], 'score': '9.1', 'comment': '(354920人评价)'}, '鬼子来了': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1181775734.jpg', 'movie_name': '鬼子来了', 'other_name': '2000-05-12(戛纳电影节) / 2002-04-27(日本) / 姜文 / 香川照之 / 袁丁 / 姜宏波 / 丛志军 / 喜子 / 泽田谦也 / 李海滨 / 蔡卫东 / 陈述 / 陈莲梅 / 史建全 / 陈强 / 宫路佳具 / 吴大维 / 梶冈润一 / 石山雄大 / 述平 / 姜武 / 中国大陆 / 姜文 / 139分钟...', 'release_time': ['2000-05-12(戛纳电影节)', '2002-04-27(日本)'], 'actor': ['姜文', '香川照之', '袁丁', '姜宏波', '丛志军', '喜子', '泽田谦也', '李海滨', '蔡卫东', '陈述', '陈莲梅', '史建全', '陈强', '宫路佳具', '吴大维', '梶冈润一', '石山雄大', '述平', '姜武', '中国大陆', '姜文', '139分钟...'], 'score': '9.2', 'comment': '(334681人评价)'}, '两杆大烟枪': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792443418.jpg', 'movie_name': '两杆大烟枪', 'other_name': '1998-08-28(英国) / 杰森·弗莱明 / 德克斯特·弗莱彻 / 尼克·莫兰 / 杰森·斯坦森 / 斯蒂文·麦金托什 / 斯汀 / 维尼·琼斯 / 丹尼·约翰-儒勒 / 维克多·麦奎尔 / 阿兰·福德 / 安德鲁·蒂曼 / 马修·沃恩 / 弗兰克·哈珀 / 罗尼·福克斯 / 罗伯·布莱顿...', 'release_time': ['1998-08-28(英国)', '杰森·弗莱明'], 'actor': ['德克斯特·弗莱彻', '尼克·莫兰', '杰森·斯坦森', '斯蒂文·麦金托什', '斯汀', '维尼·琼斯', '丹尼·约翰-儒勒', '维克多·麦奎尔', '阿兰·福德', '安德鲁·蒂曼', '马修·沃恩', '弗兰克·哈珀', '罗尼·福克斯', '罗伯·布莱顿...'], 'score': '9.1', 'comment': '(352235人评价)'}, '被嫌弃的松子的一生': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p453723669.jpg', 'movie_name': '被嫌弃的松子的一生', 'other_name': '2006-05-27(日本) / 中谷美纪 / 瑛太 / 香川照之 / 市川实日子 / 伊势谷友介 / 柄本明 / 黑泽明日香 / 荒川良良 / 柴崎幸 / 土屋安娜 / 奥之矢佳奈 / 谷原章介 / 武田真治 / 片平渚 / 宫藤官九郎 / 角野卓造 / 田中要次 / 木村凯拉 / 谷中敦...', 'release_time': ['2006-05-27(日本)', '中谷美纪'], 'actor': ['瑛太', '香川照之', '市川实日子', '伊势谷友介', '柄本明', '黑泽明日香', '荒川良良', '柴崎幸', '土屋安娜', '奥之矢佳奈', '谷原章介', '武田真治', '片平渚', '宫藤官九郎', '角野卓造', '田中要次', '木村凯拉', '谷中敦...'], 'score': '8.9', 'comment': '(414122人评价)'}, '活着': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2513253791.jpg', 'movie_name': '活着', 'other_name': '1994-05-17(戛纳电影节) / 1994-06-30(香港) / 葛优 / 巩俐 / 姜武 / 牛犇 / 郭涛 / 张璐 / 倪大红 / 肖聪 / 董飞 / 刘天池 / 董立范 / 黄宗洛 / 刘燕瑾 / 李连义 / 杨同顺 / 苏岩 / 王丽华 / 中国大陆 / 香港 / 张艺谋 / 132分钟 / 剧情 / 历史 / 家庭...', 'release_time': ['1994-05-17(戛纳电影节)', '1994-06-30(香港)'], 'actor': ['葛优', '巩俐', '姜武', '牛犇', '郭涛', '张璐', '倪大红', '肖聪', '董飞', '刘天池', '董立范', '黄宗洛', '刘燕瑾', '李连义', '杨同顺', '苏岩', '王丽华', '中国大陆', '香港', '张艺谋', '132分钟', '剧情', '历史', '家庭...'], 'score': '9.2', 'comment': '(409160人评价)'}, '楚门的世界': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg', 'movie_name': '楚门的世界', 'other_name': '1998-06-05(美国) / 金·凯瑞 / 劳拉·琳妮 / 艾德·哈里斯 / 诺亚·艾默里奇 / 娜塔莎·麦克艾霍恩 / 马西娅·德波尼斯 / Adam Tomei / 哈里·谢尔 / 约翰·普莱舍 / 澳澜·琼斯 / Joe Minjares / 特里·金瑞利 / 乔尔·麦金农·米勒 / 冈本玉二 / Jake Eberle...', 'release_time': ['1998-06-05(美国)', '金·凯瑞'], 'actor': ['劳拉·琳妮', '艾德·哈里斯', '诺亚·艾默里奇', '娜塔莎·麦克艾霍恩', '马西娅·德波尼斯', 'Adam Tomei', '哈里·谢尔', '约翰·普莱舍', '澳澜·琼斯', 'Joe Minjares', '特里·金瑞利', '乔尔·麦金农·米勒', '冈本玉二', 'Jake Eberle...'], 'score': '9.2', 'comment': '(755718人评价)'}, '搏击俱乐部': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910926158.jpg', 'movie_name': '搏击俱乐部', 'other_name': '1999-09-10(威尼斯电影节) / 1999-10-15(美国) / 爱德华·诺顿 / 布拉德·皮特 / 海伦娜·伯翰·卡特 / 扎克·格雷尼尔 / 米特·洛夫 / 杰瑞德·莱托 / 艾恩·贝利 / 里奇蒙德·阿奎特  / 乔治·马奎尔 / 鲍勃·斯蒂芬森 / Carl Ciarfalio / 斯图尔特·布拉姆博格...', 'release_time': ['1999-09-10(威尼斯电影节)', '1999-10-15(美国)'], 'actor': ['爱德华·诺顿', '布拉德·皮特', '海伦娜·伯翰·卡特', '扎克·格雷尼尔', '米特·洛夫', '杰瑞德·莱托', '艾恩·贝利', '里奇蒙德·阿奎特 ', '乔治·马奎尔', '鲍勃·斯蒂芬森', 'Carl Ciarfalio', '斯图尔特·布拉姆博格...'], 'score': '9.0', 'comment': '(514373人评价)'}, '死亡诗社': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910824340.jpg', 'movie_name': '死亡诗社', 'other_name': '1989-06-02(多伦多首映) / 1989-06-09(美国) / 罗宾·威廉姆斯 / 罗伯特·肖恩·莱纳德 / 伊桑·霍克 / 乔西·查尔斯 / 盖尔·汉森 / 迪伦·库斯曼 / 阿勒隆·鲁杰罗 / 詹姆斯·沃特斯顿 / 诺曼·劳埃德 / 柯特伍德·史密斯 / 卡拉·贝尔韦尔 / 利昂·波纳尔...', 'release_time': ['1989-06-02(多伦多首映)', '1989-06-09(美国)'], 'actor': ['罗宾·威廉姆斯', '罗伯特·肖恩·莱纳德', '伊桑·霍克', '乔西·查尔斯', '盖尔·汉森', '迪伦·库斯曼', '阿勒隆·鲁杰罗', '詹姆斯·沃特斯顿', '诺曼·劳埃德', '柯特伍德·史密斯', '卡拉·贝尔韦尔', '利昂·波纳尔...'], 'score': '9.0', 'comment': '(388695人评价)'}, 'V字仇杀队': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1465235231.jpg', 'movie_name': 'V字仇杀队', 'other_name': '2005-12-11(BNAT电影节) / 2006-03-17(美国) / 娜塔莉·波特曼 / 雨果·维文 / 斯蒂芬·瑞 / 斯蒂芬·弗雷 / 约翰·赫特 / 蒂姆·皮戈特-史密斯 / 鲁珀特·格雷夫斯 / 罗杰·阿拉姆 / 本·迈尔斯 / 西妮德·库萨克 / 娜塔莎·怀特曼 / 约翰·斯坦丁 /...', 'release_time': ['2005-12-11(BNAT电影节)', '2006-03-17(美国)'], 'actor': ['娜塔莉·波特曼', '雨果·维文', '斯蒂芬·瑞', '斯蒂芬·弗雷', '约翰·赫特', '蒂姆·皮戈特-史密斯', '鲁珀特·格雷夫斯', '罗杰·阿拉姆', '本·迈尔斯', '西妮德·库萨克', '娜塔莎·怀特曼', '约翰·斯坦丁 /...'], 'score': '8.8', 'comment': '(593760人评价)'}, '闻香识女人': {'poster': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2550757929.jpg', 'movie_name': '闻香识女人', 'other_name': '1992-12-23(美国) / 阿尔·帕西诺 / 克里斯·奥唐纳 / 詹姆斯·瑞布霍恩 / 加布里埃尔·安瓦尔 / 菲利普·塞默·霍夫曼 / 理查德·文彻 / 布莱德利·惠特福德 / 罗谢尔·奥利弗 / 托德·路易斯 / 马特·史密斯 / 吉恩·坎菲尔德 / 弗兰西丝·康罗伊...', 'release_time': ['1992-12-23(美国)', '阿尔·帕西诺'], 'actor': ['克里斯·奥唐纳', '詹姆斯·瑞布霍恩', '加布里埃尔·安瓦尔', '菲利普·塞默·霍夫曼', '理查德·文彻', '布莱德利·惠特福德', '罗谢尔·奥利弗', '托德·路易斯', '马特·史密斯', '吉恩·坎菲尔德', '弗兰西丝·康罗伊...'], 'score': '9.0', 'comment': '(457858人评价)'}, '低俗小说': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910902213.jpg', 'movie_name': '低俗小说', 'other_name': '1994-05-12(戛纳电影节) / 1994-10-14(美国) / 约翰·特拉沃尔塔 / 乌玛·瑟曼 / 阿曼达·普拉莫 / 蒂姆·罗斯 / 塞缪尔·杰克逊 / 菲尔·拉马 / 布鲁斯·威利斯 / 弗兰克·威利 / 布尔·斯蒂尔斯 / 文·瑞姆斯 / 劳拉·拉芙蕾丝 / 保罗·考尔德伦...', 'release_time': ['1994-05-12(戛纳电影节)', '1994-10-14(美国)'], 'actor': ['约翰·特拉沃尔塔', '乌玛·瑟曼', '阿曼达·普拉莫', '蒂姆·罗斯', '塞缪尔·杰克逊', '菲尔·拉马', '布鲁斯·威利斯', '弗兰克·威利', '布尔·斯蒂尔斯', '文·瑞姆斯', '劳拉·拉芙蕾丝', '保罗·考尔德伦...'], 'score': '8.8', 'comment': '(460328人评价)'}, '美丽心灵': {'poster': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1665997400.jpg', 'movie_name': '美丽心灵', 'other_name': '2001-12-13(加州首映) / 2002-01-04(美国) / 罗素·克劳 / 艾德·哈里斯 / 詹妮弗·康纳利 / 克里斯托弗·普卢默 / 保罗·贝坦尼 / 亚当·戈德堡 / 乔什·卢卡斯 / 安东尼·拉普 / 贾森·加里-斯坦福德 / 贾德·赫希 / 奥斯汀·潘德尔顿 / 薇薇·卡登尼...', 'release_time': ['2001-12-13(加州首映)', '2002-01-04(美国)'], 'actor': ['罗素·克劳', '艾德·哈里斯', '詹妮弗·康纳利', '克里斯托弗·普卢默', '保罗·贝坦尼', '亚当·戈德堡', '乔什·卢卡斯', '安东尼·拉普', '贾森·加里-斯坦福德', '贾德·赫希', '奥斯汀·潘德尔顿', '薇薇·卡登尼...'], 'score': '8.9', 'comment': '(411983人评价)'}}


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

**3. xpath**  
 - "//"  # 代表从根节点搜索
 - "//a"  # 搜索根节点的所有a标签
 - "//a[@class="nbg]"  # 搜索class="nbg"的a标签
 - ".../a"  # 搜索从...节点开始的子a标签
 - ".../img/@src"  # 获取当前img标签的src属性
 - ".../p/text()"  # 获取当前p标签下的文本
 - ".../p//text()"  # 获取当前p标签后的所有文本(子孙文本)

**4. pyquery**  
  - "a.nbg"  # 表示 a class="nbg"
  - "a img"  # 表示 a标签的子孙img标签
  - .remove()  # 表示移除该节点
  - .items()  # 当选中多个节点时,需要使用.items() 生成可遍历对象再进行提取
  - .attr()  # 表示获取标签
  - .text()  # 表示获取文本

**5. 混合提取**  
   - .css()  # 就是css规则的提取
   - .xpath()  # 就是xpath规则的提取,需要注意的是,因为scrapy的Selector支持混用,如果xpath是在某个提取器之后,那么必须使用"./"来跟进上个提取器的提取点,不能使用"//", 因为Selector 的xapth提取器的"//"永远代表根节点
       - response.css("#id").xpath("./a")  # 该规则表示id="id" 的节点**之后**的所有a标签节点
       - response.css("#id").xpath("//a")  # 改规则就变成了提取所有的a标签节点,前面的css选择器的结果失效.
   - .re()  # 就是正则的提取, 正则提取后,不需要用extract()来转化成str类型
   - extract()  # 将当前的选择结果转化成str类型  
