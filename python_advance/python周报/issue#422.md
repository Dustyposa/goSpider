### 欢迎阅读《pythonista周刊》第422期。Let us start!


>原文: [https://mailchi.mp/pythonweekly/python-weekly-issue-422](https://mailchi.mp/pythonweekly/python-weekly-issue-422)  
>翻译：Dustyposa

### 来自赞助商:
使用 `Datadog` 监控你的python指标，日志，集群分析。使用`Datadog`的应用分析，可以深入任何纬度并且能找到你所需要的信息，来进行动态诊断和快速故障排除。[马上跟踪你的python应用吧！免费试用14天哦！](https://www.datadoghq.com/dg/apm/ts-python-tracing/?utm_source=Advertisement&utm_medium=Advertisement&utm_campaign=PythonWeekly-Tshirt)
> 熟悉的面孔。
## 新闻
####  [Python 采用 12 个月的发布周期](https://pythonweekly.us2.list-manage.com/track/click?u=e2e180baf855ac797ef407fc7&id=fea677de77&e=57c131a127)
> Python 升级固定了！

#### [在银行Python 已经取代了 Excel](https://pythonweekly.us2.list-manage.com/track/click?u=e2e180baf855ac797ef407fc7&id=85e5cd4508&e=57c131a127) 

> 就是在某些银行，已经只用`Python`来处理数据了！原因其实很简单，就是`Excel`太慢了。。想想用`Excel`处理大型文件，内心是绝望的！
>
> 该来的还是会来的！



## 文章、教程与话题
####  ["Writing a PEG parser for fun and profit" - Guido van Rossum](https://www.youtube.com/watch?v=QppWTvh7_sI)  ![img](https://gallery.mailchimp.com/e2e180baf855ac797ef407fc7/images/8def3887-e9e9-4a48-95e0-74045a6a23fc.png)(42 min)

解析表达文法(PEGs) 是一种新的用来描述适合自动生成高效解析器的文法的形式。我对使用 基于PEG生成器的解析器来代理在`Cython`中使用近30年的"pgen"解析生成器很有兴趣。这出现了一些有趣的问题。我还想出了一种可视化解析过程的简单方法，它有助于调试文法和解析机制，并且我将使用它去解释一般的`PEG`解析过程。

> 龟叔依然很忙~

####  [不要使用 utcnow and utcfromtimestamp](https://blog.ganssle.io/articles/2019/11/utcnow.html) 
关于`utcnow`和`utcfromtimestamp`的危险以及使用其替代品的好处的公共服务公告。
> utc 的坑，国际化的Application不易呀~

####  [JWT 认证和 DjangoREST API](https://t.co/zT2Lxr3Us1) 
基于 Token  的身份认证允许服务器和前端（无论是网络、本地移动设备还是其他设备）分离，并归属于不同的域名。`JSON Web Tokens(JWT)`是基于 token 的身份认证的一种常见实现方式，在这篇文章，我们将会用它在一个基于`Django REST`框架的notes应用中的一个API进行用户认证。
> 熟悉的实践篇章

####  [通过做5个游戏来学习 Python](https://www.youtube.com/watch?v=XGf2GcyHPhc) ![img](https://gallery.mailchimp.com/e2e180baf855ac797ef407fc7/images/8def3887-e9e9-4a48-95e0-74045a6a23fc.png)（6h43min）

在这个面向初学者的完整教程中学习`Python`。这个课程使用的是以项目为基础的方法。我们一共收集了5个很好的`Python`游戏教程，所以你可以在构建5个游戏的同时学习`Python`。你如果是实践学习者，这个课程非常适合你！

> 寓教于乐

#### [Python range 指南：学习使用这个很有用的内置函数](https://www.dataquest.io/blog/python-range-tutorial/)
在这篇详细的指南中，我们将通过几个栗子来带你了解`range`函数的工作原理，并探讨它的局限及解决办法。`range`对各种各样的`Python编程任务`来说都是很有用的，该指南最后将介绍以`range函数`在数据科学的应用的几个栗子。
> 又一篇新手推荐~

####  [通过GitHub Actions，Poetry，Black和Pytest快速实现CI](https://t.co/GiXdUiDQrm)  
为`Django`项目设置`Github Actions`
> 部署上线一条龙~

####  [通过 Python 理解 OpenGL](https://stackabuse.com/understanding-opengl-through-python/) 
如何使用`Spectrograms和GANs`将爵士乐转换成古典乐
> 不知道 MIKU 的音乐能不能转~


####  [Python Datetime 指南: 操作 Times, Dates 和 Time Spans](https://www.dataquest.io/blog/python-datetime-tutorial/)  
在本数据科学教程中使用`datetime和calender`模块成为成为`Python`中的时间和日期的大师。

> 希望能操作虫洞！

####  [Python: 超乎想象的 typed](https://beepb00p.xyz/mypy-error-handling.html) 
`mypy`辅助错误处理，其他语言中的异常机制，模式匹配和类型差异的乐趣。

> 何以解忧，唯有`mypy`

#### [为什么你应该使用 `python -m pip`](https://snarky.ca/why-you-should-use-python-m-pip/)
该文章揭示了什么是`python -m pip`和你为什么在运行`pip`的时候应该使用它。

> 环境比较重要

#### [基于Keras和深度学习的交通标志分类](https://www.pyimagesearch.com/2019/11/04/traffic-sign-classification-with-keras-and-deep-learning/)

在本片指南，你讲学习到如何训练你自己的交通标志分类器/识别器，使用`Keras和深度学习`可以使其可以达到95%以上的准确率。

> 哪里不认识训练哪里！

#### [我们如何发现并修复Python代码中的性能下降](https://blog.redash.io/how-we-spotted-and-fixed-a-performance-degradation-in-our-python-code/)

> 实践出真理

#### [用Python进行医疗保险欺诈检测](https://www.theseattledataguy.com/healthcare-fraud-detection-with-python/)

> 人心叵测～

#### [Python标准库中一些鲜为人知的地方](https://t.co/vbMM7hNrJG)

> 骚操作finding！

#### [Hugging Face: TensorFlow 2.0使用10行代码实现最先进的nlp处理](https://blog.tensorflow.org/2019/11/hugging-face-state-of-art-natural.html)

> 适合简单了解一下～

#### [在 Python 中通过源码和行号找到定义](https://julien.danjou.info/finding-definitions-from-a-source-file-and-a-line-number-in-python/)

> 文法分析，语法树～最近在看的

#### [你不需要迁移至 Python 3](https://switowski.com/blog/you-dont-have-to-migrate-to-python3)

> 所以我是升还是不升呢？



## 有趣的项目、工具和库

####  [Spleeter](https://github.com/deezer/spleeter)  

`Spleeter`是 `Deezer`的源分离库，有用`Python`使用`Tensorflow`编写的预训练模型。让训练一个源分离模型（ 假设已经有了一个隔离源的数据集 ）变得容易。并且提供了已经训练好的用于执行各种分离风格的最新模型。

> 音轨分离！佳作。
>
> 内置3种分离模式。可以自由选择哦！
>
> 听不出自己声音的我估计是没戏了。

####  [inbac](https://github.com/weclaw1/inbac) 
`inbac`是一款交互式批量裁剪器，用于快速裁剪图像。

> 剪裁太慢？python来凑！



####  [trains-agent](https://github.com/allegroai/trains-agent) 

它是一种零配置的“一劳永逸”执行代理，与trains-server结合使用可提供完整的AI集群解决方案。

> AI服务也是需要Dev-ops的，为什么？因为都是集群了！
>
> 
>
> 

#### [python-gift-exchange](https://github.com/sethblack/python-gift-exchange) 

Python礼物交换选择器

> 一个程序员被妻子逼迫的故事！
>
> 没办法，为什么自己这么强呢？（不是我！！！！！！）



####   [jsonfield-schema](https://github.com/viewflow/jsonfield-schema) 

从任何图片查找主色调。

> 之前在 trending 看到过，百宝箱。

#### [PySlowFast](https://github.com/facebookresearch/SlowFast)
`PySlowFast` 是一个来自`FAIR`开源的视频理解代码库。它提供了最先进的视频分类模型，包括了论文`SlowFast Networks for Video Recognition ` 和 `Non-local Neural Networks.` 

> 学术+工业？
>
> 如图，看一看前沿的操作：
>
> ![421ava_demo.gif](https://i.loli.net/2019/11/03/xgYCfMuZI6o5TGy.gif)

#### [flask_api_example](https://github.com/apryor6/flask_api_example)
大型`Flask API`项目的最佳实践演示。

> 别犹豫了，你们要的来了！

#### [PyPong](https://github.com/skamieniarz/pypong)

用`Python`和`pyxel`实现的稍作修改的克隆版，经典的`Pong`游戏。

> 复古与回忆～

#### [napari](https://github.com/napari/napari)

用`Python`实现的一个快速，可交互的多维图片查看器。

> 还在 alpha 阶段，还是一张图了解一下（什么不好用就造什么！）～
>
> ![421screenshot-add-image.png](https://i.loli.net/2019/11/03/5J6xLwNAgrlV8KU.png)
>
> 

#### [WhatsApp_emoji_ranker](https://github.com/DerRiedi/WhatsApp_emoji_ranker)

一个简单的程序，可以解析从`Whatsapp`导出的`.txt`文件，并且提取`emojis`并根据其频率生产条形图（使用的：`matplotlib`）

> 一张图快速了解～
>
> ![421emoji_hist.png](https://i.loli.net/2019/11/03/VSmNHwBW9ru8pOc.png)
>
> 

## 活动和网络研讨会日程

#### [PyCon Canada 2019](https://2019.pycon.ca/) 

想让你自己沉迷于两天的精彩演讲、特别的主题演讲，不可思议的赞助商，以及其他兴趣相似的`Pythonista`吗？

想要了解更多？加入我们周一和周二（11月 18-19）的开发`sprints`，一个你和你的`Python`小伙伴可以在有趣的团队氛围中参与开源的个人项目的地方。

> 心动不如心动！踏上 2019 的末班车～

#### [Effortless REST W/ Flask - Charlotte, NC](https://www.meetup.com/PyDataCharlotte/events/265952190/)

你是`Python`新手，并想自己构建一些很酷的东西吗？你想知道构建真实为生产环境准备的`API`需要什么吗？你对如何通过`API`实现你最新的想法有疑问吗？你想在45分钟实现吗？如果是的，这次的`talk`就是为你准备的！

> 教练！我想做`API`


## Posa：
> ❤️ Happy Pythonic ;-(Posa私人无责任播报)
#### [测测你的python数据类型掌握了吗！](https://realpython.com/quizzes/python-data-types/viewer/)

一个测试~哎，有点难，可以试试，8道题，3分钟差不多。是时候展现自己真正的实力了。




----- 分割线 -----
> 如果你发现哪里翻译有误的话，请务与我联系！感谢！
>
> 




