Title: pythonista-weekly : Pyw 432
Date: 2020-01-11 15:16
Tags: Weekly,pythonweekly,Zh 
Slug: pyw-432

### 欢迎阅读《pythonista周刊》第432期。Let us start!


>原文: [https://mailchi.mp/pythonweekly/python-weekly-issue-432](https://mailchi.mp/pythonweekly/python-weekly-issue-432)  
>翻译：Dustyposa

### 来自赞助商（PS：原文的赞助商）:

使用 `Datadog` 监控你的python指标，日志，集群分析。使用`Datadog`的应用分析，可以深入任何纬度并且能找到你所需要的信息，来进行动态诊断和快速故障排除。[马上跟踪你的python应用吧！免费试用14天哦！](


## 文章、教程与话题

[Mercurial's Journey to and Reflections on Python 3](https://gregoryszorc.com/blog/2020/01/13/mercurial's-journey-to-and-reflections-on-python-3/)
Mercurial 5.2 was released on November 5, 2019. It is the first version of Mercurial that supports Python 3. This milestone comes nearly 11 years after Python 3.0 was first released on December 3, 2008. This post is logically divided into two sections: a mostly factual recount of Mercurial's Python 3 porting effort and a more opinionated commentary of the transition to Python 3 and the Python language ecosystem as a whole. 

[Managing Python Environments](https://www.pluralsight.com/tech-blog/managing-python-environments/)
If you're not careful, your Python environment can quickly become a disaster.  We'll walk through the available tools to be more (code) environmentally friendly and establish some (highly opinionated) preferences for setting up Python.

[Passing a function as an argument to another function in Python](https://treyhunner.com/2020/01/passing-functions-as-arguments/)
One of the more hair-raising facts we learn in my introductory Python trainings is that you can pass functions into other functions. You can pass functions around because in Python, functions are objects. You likely don’t need to know about this in your first week of using Python, but as you dive deeper into Python you’ll find that it can be quite convenient to understand how to pass a function into another function. This is part 1 of what I expect to be a series on the various properties of “function objects”. This article focuses on what a new Python programmer should know and appreciate about the object-nature of Python’s functions.

[Easy Visual Question Answering](https://victorzhou.com/blog/easy-vqa/)
A gentle introduction to Visual Question Answering (VQA) using neural networks.

[Ultimate Setup for Your Next Python Project](https://martinheinz.dev/blog/14)
Whether you are working on some machine learning/AI stuff, building web apps in Flask or just writing some quick Python script, it's always useful to have some template for your project that satisfies all your needs, namely: predefined directory structure, all necessary config files like pytest.ini or requirements.txt, Testing, linting and static code analysis setup, CI/CD tooling, Dockerization of your app and on top of that automation with Makefile. So, here I bring you exactly that in this "Ultimate" all-purpose setup for your Python projects.

[From Browser To Django](https://www.mattlayman.com/understand-django/browser-to-django/)
Django helps you build websites in Python. How does it work? In this series, we'll explore Django from top to bottom to show you how to build the website you've wanted. We'll start from the beginning with the browser.

[Django 3 Tutorial & CRUD Example with MySQL and Bootstrap](https://www.ahmedbouchefra.com/blog/django-3-tutorial-and-crud-example-with-mysql-and-bootstrap/)
Django 3 is released with full async support! In this tutorial, we’ll see by example how to create a CRUD application from scratch and step by step. We’ll see how to configure a MySQL database, enable the admin interface, and create the django views.

[The Eurotrip Planner- Part 1](https://shreyasgokhale.com/tech-blog/eurotrip-planner-part-1)
A Python script to help you find your ideal EuroTrip.

- [The Eurotrip Planner- Part 2](https://shreyasgokhale.com/tech-blog/eurotrip-planner-part-2)

[从监狱到Python我学到了什么](https://opensource.com/article/20/1/prison-to-python)
开源编程如何在入狱后提供机会。

> 真 从XX到YY系列！

[Redis Server-Assisted Client-Side Caching in Python](https://engineering.redislabs.com/posts/redis-assisted-client-side-caching-in-python/)

[Guide: Optimizing Python Code with ctypes](https://samuelstevens.me/writing/optimizing-python-code-with-ctypes)

[How python implements super long integers?](https://arpitbhayani.me/blogs/super-long-integers)

[How to Build GraphQL APIs for Text Analytics in Python](https://atheros.ai/blog/how-to-build-graphql-api-for-text-analytics-in-python)



## 有趣的项目、工具和库

**[scalene](https://github.com/emeryberger/scalene)**

适用于`Python`的高性能，高精度CPU和内存分析器。

> 久违的性能分析！



**[Slacky](https://github.com/M4cs/Slacky)**
第一个用于`Slack`工作区的`Python Selfbot`。 创建`Slacky`是为了使`Slack`自动化并使其更有趣。 默认情况下，它附带许多命令，甚至允许轻松构建和导入自定义插件。

> 用着不变，Python来遍！

**[speck](https://github.com/lucashadfield/speck)**

将图像渲染为一组连续的线，代表像素的每个水平（或垂直）线。

> 从点到线！自然转变！

**[Spotipy](https://github.com/plamere/spotipy)**

用于`Spotify Web API`的一个轻量级的`Python`库。

> 肯定是上面那个的兄弟！

**[CrossHair](https://github.com/pschanely/CrossHair)**

用于`Python`的静态分析工具，模糊了测试系统和类型系统之间的界限。

> 上上上上



**[CleverCSV](https://github.com/alan-turing-institute/CleverCSV)** 

CleverCSV通过改进对杂乱CSV文件的`dialect`检测功能，为`Python` csv软件包提供了直接替代。 它还提供了一个方便的命令行工具，该工具可以标准化凌乱的文件或生成Python代码以将其导入。

> CSV数据处理恐惧症的福音！



**[Array_Visualizer](https://github.com/Sklyvan/Array_Visualizer)**

可视化数组，使用常用的排序算法来可视化这些算法是如何工作的。

> 很熟悉，之前有个JS库也是这么干过！

**[AutoGluon](https://github.com/awslabs/autogluon)**

`AutoGluon`有易于使用和易于扩展的`AutoML`，并将重点放在跨越图像，文本或表格数据的深度学习和实际应用中。

**[SpoTUI](https://github.com/ceuk/spotui)**

另一个基于终端的Spotify客户端。



## 活动和网络研讨会日程

[Parsl: Pervasive Parallel Programming in Python - Chicago, IL](https://www.meetup.com/PyDataChi/events/267549801/)

[PyHou Meetup January 2020 - Houston, TX](https://www.meetup.com/python-14/events/ndcfkrybccbcc/)

[Data Visualization with Altair: a grammar of graphics for Python - Madison, WI](https://www.meetup.com/PyData-Madison/events/267088359/)

[San Diego Python Meetup January 2020 - San Diego, CA](https://www.meetup.com/pythonsd/events/xrtzkrybccbfc/)

## Posa：

> ❤️ Happy Pythonic ;-(Posa私人无责任播报)  

热腾腾的协程翻译: **[异步爬虫](https://github.com/Dustyposa/goSpider/blob/master/python_advance/%E7%BF%BB%E8%AF%91%E8%AE%A1%E5%88%92/%E5%BC%82%E6%AD%A5%E7%88%AC%E8%99%AB)**

初次翻译，多多指教，发现问题请提提提出来！！谢谢各位大佬了。

----- 分割线 -----

> 如果你发现哪里翻译有误的话，请务与我联系！感谢！
>




- 首发: [pythonista-weekly~蠎周刊 ~汇集全球蠎事儿 ;-)](http://weekly.pychina.org/python-weekly/pyw-432.html)
- 改进: [issue-432.md](https://github.com/PyChina/weekly/blob/master/content/python-weekly/issue#432.md)


