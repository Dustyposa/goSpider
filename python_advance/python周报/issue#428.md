Title: pythonista-weekly : Pyw 428
Date: 2019-12-14 15:16
Tags: Weekly,pythonweekly,Zh 
Slug: pyw-428

### 欢迎阅读《pythonista周刊》第428期。Let us start!


>原文: [https://mailchi.mp/pythonweekly/python-weekly-issue-428](https://mailchi.mp/pythonweekly/python-weekly-issue-428)  
>翻译：Dustyposa

### 来自赞助商（PS：原文的赞助商）:
**[python开发者都需要的Vettery](https://www.vettery.com/tech?utm_source=newsletter&utm_medium=pythonweekly&utm_term=tech&utm_content=grouped&utm_campaign=ad-77579)**  

Vettery是一个招聘网站，它改变了人们应聘或者雇佣的方式。准备好换工作地方了吗？免费制作简历，你的薪资你说了算，现在就和顶级雇主的HR联系吧！



## 新闻

**[SciPy 2020 意见征集](https://www.scipy2020.scipy.org/)**

征求建议书截止到2020年2月11日。




## 文章、教程与话题
**[训练自定义dlib形状预测器](https://www.pyimagesearch.com/2019/12/16/training-a-custom-dlib-shape-predictor/)**

在本篇教程中，你将学习如何训练你自己的自定义`dlib`形状预测器*(shape predictor)*。然后你将学习如何拿到的经过训练的`dlib`形状预测器，并使用它去预测输入的图像和实时视频流的坐标。

> 微妙的五官捕捉。

**[如何使用Django 框架做密码校验](https://www.youtube.com/watch?v=SRYBDmJlIck) ![img](https://gallery.mailchimp.com/e2e180baf855ac797ef407fc7/images/8def3887-e9e9-4a48-95e0-74045a6a23fc.png)*(15min)***

`Django`有内置的密码校验功能。这个视频演示了如何开启并配置校验，自定义校验设置，编写你自己的校验器，并将验证集成到你自己的接口或者`API`中。

> Django 内置了很多工具，来瞅一下。

**[用数据科学的方法计算出一辆二手车的合理价格](https://t.co/sVcObePjlO)** 

使用`DS`*（译者注：应该是`data science`的缩写。。）*方法计算二手车公平价格的整个过程。

> 似曾相识。

**[100万对任何人来说都应该足够了](https://lwn.net/SubscriberLink/807218/7589bd420fa9cfbe/)**

编程语言在其操作的各种方面通常都会有些显示或者隐式的限制。比如标识符*(identifier)*的最大长度或者一个变量可以存储的值的范围等明显的例子，但是还有其他的，其中许多不是语言设计者指定的，但是来自语言的各种实现。这种模棱两可会出现问题，所以在`Python`中确定各种各样的限制是当前在`python-dev`邮件列表中持续讨论的目标。

> 左右两难
>
> 不过巧了，最新的 捕蛇者说 (Ep09) 有提到这个问题。



**[劫持(hijacking)Django 默认的'Through' Tables](https://typenil.com/hijacking-default-django-through-tables/)**

去年有几次我遇到了需要向一个`Django`多对多关系中添加一些元数据。默认情况下，没有明确的模型可以添加字段，但是如果你在开发一个灵活的项目-在默认的`through`表中存在一些数据，你并不想丢失这些数据。所以，如果你不想创建一个新的表并迁移数据该怎么解决呢？让我们劫持一个！

> 不够打补丁。



[Why do people Love the Powerful Python Newsletter?](https://powerfulpython.com/newsletter/?utm_source=pythonweekly&utm_medium=newsletter&utm_campaign=2019-12-19)
"Thanks for the awesome newsletter! I look forward to your emails." "Python needs tougher treatment than what's out there. Keep going, don’t ever stop." For Intermediate Python. Subscribe free now. SPONSOR

[How I saved Christmas with the Travelling Salesman Problem](https://t.co/LGeDuqINzt) 
A nice visualization of the Santa’s optimal trip.

[Build a CRUD application using Vue and Django](https://codesource.io/build-a-crud-application-vue-and-django/)
This tutorial shows you how to build an API with Django REST Framework and a SPA with Vue.js.

[Easy web scraping with Scrapy](https://www.scrapingbee.com/blog/web-scraping-with-scrapy/)
Scrapy is the most popular Python web scraping framework. In this tutorial we will see how to scrape an E-commerce website with Scrapy from scratch.

[CPython Segfault in 5 lines of code](https://gist.github.com/coolreader18/6dbe0be2ae2192e90e1a809f1624c694)

[A Tiny Python Exception Oddity](https://aroberge.blogspot.com/2019/12/a-tiny-python-exception-oddity.html)

[Finding Natural Breaks in Data with the Fisher-Jenks Algorithm](https://pbpython.com/natural-breaks.html)

[Using pyenv to manage your Python interpreters](https://www.marc-richter.info/using-pyenv-to-manage-your-python-interpreters/)

[Experiments in Constraint-based Graphic Design](https://www.anishathalye.com/2019/12/12/constraint-based-graphic-design/)

[Reducing NumPy memory usage with lossless compression](https://pythonspeed.com/articles/numpy-memory-footprint/)



## 有趣的项目、工具和库

[AI Dungeon 2](https://github.com/AIDungeon/AIDungeon)

`AI Dungeon 2`是一个完全由`OpenAI最大的GPT-2模型`构建的`AI`生成的文字冒险游戏。这是同类游戏中的第一个，它允许你输入并对任何你能想象的动作作出反应。

> Colab 能直接玩哦！

[Mario: Shell pipes in Python](https://github.com/python-mario/mario)

你曾经想过直接在你的`Unix shell`种直接使用`Python函数`？`Mario`可以读写`csv,json and yaml`;遍历树，甚至进行`xpath`查询。另外，它还支持开箱即用的`async`命令。用一个简单的配置文件构建你自己的命令，并安装更多的插件吧！

> 随处可用`Python`的时代？

[Informer](https://github.com/paulpierre/informer) 

一个用`Python`编写的`Telegram Mass Surveillance`机器人。

> 做数据分析用的～

[awspx](https://github.com/FSecureLABS/awspx)

一个用于可视化`AWS`环境中的有效访问和资源关系的基于图的工具。

> AWS很强啊

[Pixcryption](https://github.com/M4cs/pixcryption)

`Pixcryption`的目标是通过图像提供一种的新型的隐写术/加密方式*(steganography/encryption)*.它使用一个随机种子的`UUID`去生成一个`user_key`，它匹配`RGB`的完美值来匹配`unicode 字符`。这些都存住在一个用于加密解密消息的`user_key.png`文件中。

> 像素加密之后会是什么！视频加密？语音加密？

[PyFlow](https://github.com/wonderworks-software/PyFlow) 

用于`Python`的可视化脚本框架。

[pydeps](https://github.com/thebjorn/pydeps)

`Python`模块依赖可视化。

> 可视化全家桶！达成！

[video-to-pose3D](https://github.com/zh-plus/video-to-pose3D)

一键实现视频转3d姿势。

[omnibot](https://github.com/lyft/omnibot)
Slack代理和Slack bot框架。

[GoCheese](http://gocheese.cypherpunks.ru/) 

一个`Python`私有软件包存储库和缓存代理。

> 搭建私人仓库可以看看。

[Horology](https://github.com/mjmikulski/horology)
方便地测量你的for循环、上下文和函数的时间。

[Maze-Generator](https://github.com/Perseus-Perry/Maze-Generator)

一个用于生成随机迷宫的脚本。（偶然间发明的。）

> 可恶的偶然！

[SparkTorch](https://github.com/dmmiller612/sparktorch)

在`Apache Spark`上训练和运行`Pytorch`模型。

> 针对性。。

[django_vue_generator](https://github.com/pawnhearts/django_vue_generator)

为`django rest 框架项目`生成`vue`前端结构。为你的序列化器和视图集以及通过`vue-resource`调用`api`的方法生成表单(通过`vuelidate`进行验证)。



[PyTorch Elastic](https://github.com/pytorch/elastic)

PyTorch Elastic（torchelastic）是一个框架，使分布式训练任务能够以容错和弹性的方式执行。

[blender-tools](https://github.com/EmbarkStudios/blender-tools)
一个Blender加载项，其中包含用于游戏开发的工作流工具。

## **New Releases**

[Python 3.8.1rc1](https://pythoninsider.blogspot.com/2019/12/python-381rc1-is-now-available-for.html)



## 活动和网络研讨会日程

[Presentation Night @ Boston Python Meetup - Cambridge, MA](https://www.meetup.com/bostonpython/events/265925678/)
将会有以下的话题：

- Python优化选项
- 用Rust扩展Python

> pyflow?


[Optimized human learning - London, UK](https://www.meetup.com/LondonPython/events/266632570/)
间隔性重复，即在一段时间内测试知识，是我们所知道的学习科学中最重要的工具之一。现代科技，以`Anki`等间隔重复记忆软件的形式，承诺通过为每个学习者提供个性化的学习时间表，将这一技术提升到一个新的水平——但往往效果不理想。在这次演讲中，`Jacob Puthipiroj`将通过机器学习来实现间隔重复调度，这在商用软件中尚属首次。

[Lightning Talks @ NYC PyLadies - New York, NY](https://www.meetup.com/NYC-PyLadies/events/266971268/)

[PyHou Meetup December 2019 - Houston, TX](https://www.meetup.com/python-14/events/ndcfkryzqbwb/)

[San Diego Python Meetup December 2019 - San Diego, CA](https://www.meetup.com/pythonsd/events/zgtnxqyzqbjc/)

[LjPyMeetup December 2019 - Ljubljana, Slovenia](https://www.meetup.com/Ljubljana-Python-Group/events/266738849/)



## Posa：
> ❤️ Happy Pythonic ;-(Posa私人无责任播报)  

Django 3.0来啦！

[戳这里](https://docs.djangoproject.com/en/3.0/)



----- 分割线 -----

> 如果你发现哪里翻译有误的话，请务与我联系！感谢！
>




- 首发: [pythonista-weekly~蠎周刊 ~汇集全球蠎事儿 ;-)](http://weekly.pychina.org/python-weekly/pyw-428.html)
- 改进: [issue-428.md](https://github.com/PyChina/weekly/blob/master/content/python-weekly/issue#428.md)


