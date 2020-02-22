Title: pythonista-weekly : Pyw 437
Date: 2020-02-22 14:36
Tags: Weekly,pythonweekly,Zh 
Slug: pyw-437

### 欢迎阅读《pythonista周刊》第437期。Let us start!


>原文: [https://mailchi.mp/pythonweekly/python-weekly-issue-437](https://mailchi.mp/pythonweekly/python-weekly-issue-437)  
>翻译：Dustyposa

**来自赞助商（PS：原文的赞助商）:**  
[python开发者都需要的Vettery](https://www.vettery.com/tech?utm_source=newsletter&utm_medium=pythonweekly&utm_term=tech&utm_content=grouped&utm_campaign=ad-77579)  
Vettery是一个招聘网站，它改变了人们应聘或者雇佣的方式。准备好换工作地方了吗？免费制作简历，你的薪资你说了算，现在就和顶级雇主的HR联系吧！



## 新闻

**[PEP 614 -- 放松对装饰器的语法限制](https://www.python.org/dev/peps/pep-0614/)**

`Python`目前要求所有的装饰器都由一个点状的名称组成，后面可以有一个单独的调用。该`PEP`建议消除这些限制，并允许装饰者成为任何有效的表达式。

> 更自由的装饰器，不过还是看使用频次吧。


## 文章、教程与话题

**[Deep Learning (for Audio) with Python](https://www.youtube.com/playlist?list=PL-wATfeyAMNrtbkCNsLcpoAyBBRJZVlnf) ![img](https://gallery.mailchimp.com/e2e180baf855ac797ef407fc7/images/8def3887-e9e9-4a48-95e0-74045a6a23fc.png)（一共14个章节)**

在本系列中，探索`Python`编程语言中深度学习的理论和实现。本课程侧重于音频和音乐深度学习的应用，但讨论了适用于任何问题的一般算法和原理。

> 还不错的教程，播放量可以的，分的很细

**[Python Itertools之旅](https://martinheinz.dev/blog/16)**

让我们来看看两个极好的`Python`库-`itertools and more_itertools`，以及如何用它们进行数据处理。



**[在Django模板中安全地放入JavaScript数据](https://adamj.eu/tech/2020/02/18/safely-including-data-for-javascript-in-a-django-template/)**

`Django模版`经常被用来传输`JavaScript`代码。不凑巧的是，如果实现不正确，这还有了`Html`注入的风险，从而导致`XSS`(跨站点脚本)攻击。让我们看看这个问题，并看看我们可以如何用`json_script`进行修复。

> 前后端分离也是一种解决方式呀

**[遗传算法说明 : Python实现](https://hackernoon.com/genetic-algorithms-explained-a-python-implementation-sd4w374i)**

遗传算法，也被简称为`"GA"`,算法的灵感来自`Charles Darwin`的自然选择理论，该理论旨在为我们不太了解的问题找到最佳解决方案。让我们来看看如何使用`Python`编写一个简单的遗传算法实现！



**[Python中的函数重载](https://arpitbhayani.me/blogs/function-overloading)**

原生的`Python`不支持函数重载-有多个函数有着相同的名字。在这篇文章中，你将学习到我们可以在`Python`中通过装饰器，字典之类的常用语言结构如何实现并增加此功能。



**[如何使用Python,Flask,Postgres and JWT 构建一个认证服务](https://www.grizzlypeaksoftware.com/articles?id=5SCpQMgookgKNtupzNHg9K)**

在这篇文章，我们将学习如何



In this article we're going to learn how to build an OAuth service that can be used as a way to authenticate calls to an API or within a microservices architecture. In this project we will be using Python, Flask, Postgres and JWT

[2020 Gartner Magic Quadrant for Data Science and Machine Learning Platforms](https://hubs.ly/H0n2-j60)
The 2020 Gartner Magic Quadrant for Data Science and Machine Learning Platforms is now available, and Domino is named a Visionary. Read the full analysis of Domino and other vendors in the report. SPONSOR

[kNN classification using Neighbourhood Components Analysis](https://kevinzakka.github.io/2020/02/10/nca/)
A detailed explanation of Neighbourhood Components Analysis with a GPU-accelerated implementation in PyTorch.

[Python CLI Utilities with Poetry and Typer](https://www.pluralsight.com/tech-blog/python-cli-utilities-with-poetry-and-typer/)
Python is exceptionally flexible as a scripting language - let's learn how to extend simple scripts into full-featured command line utilities.

[How to scale Python multiprocessing to a cluster with one line of code](https://t.co/qCDLxnpKjb)
This post shows how multiprocessing.Pool can be seamlessly scaled from a single machine to a cluster.

[Python Tools for Record Linking and Fuzzy Matching](https://pbpython.com/record-linking.html)
This article discusses useful python tools for linking record sets and fuzzy matching on text fields. These concepts can also be used to deduplicate data.

[From the notebook of a Python charmer: How to make it dance to your speech](https://t.co/VYGoQEd23P)
Compare 9 most prominent automatic speech recognition engines. Learn which one is best for your needs, and how to use it in Python programs.

[DevOps for Data Science with GCP](https://t.co/JEEMYcNHXb)
Deploying Production-Grade Containers for Model Serving.

[Python Firebase Course For Beginners](https://www.youtube.com/watch?v=VnUXbo8JvvA) ![img](https://gallery.mailchimp.com/e2e180baf855ac797ef407fc7/images/8def3887-e9e9-4a48-95e0-74045a6a23fc.png)
In this Python Firebase Course for Beginners, we are going to work with Firebase using Python Programming Language. especially we are going to work with Firebase Real Time Database, Firebase Authentication and Firebase Storage. and also we will use pyrebase library, which is a simple python wrapper for the Firebase API. 

[Loves Me, Loves Me Not: Classify Texts with TensorFlow and Twilio](https://www.twilio.com/blog/classify-texts-with-tensorflow-and-twilio-to-answer-loves-me-loves-me-not)
This post will go over how to perform binary text classification with neural networks using Twilio and TensorFlow in Python.

[Build a custom-trained object detection model with 5 lines of code ](https://t.co/73BIfMhRgN)
Making computer vision easy with Detecto, a Python package built on top of PyTorch.

[Dissecting a Web stack](https://www.thedigitalcatonline.com/blog/2020/02/16/dissecting-a-web-stack/)

[How To Create Your Own Cheap Heroku-Clone and setup Django and Postgres on it](https://blog.alfred.software/2020/02/12/how-to-create-your-own-heroku-clone-and-setup-django-and-postgres/)

[How to Reverse a Binary Tree in Python](https://ao.gl/how-to-reverse-a-binary-tree-in-python/)

[Autoencoders with Keras, TensorFlow, and Deep Learning](https://www.pyimagesearch.com/2020/02/17/autoencoders-with-keras-tensorflow-and-deep-learning/)

[Uniquely Managing Test Execution Resources using WebSockets](https://tryexceptpass.org/article/manage-test-resources-with-websockets/)

## 有趣的项目、工具和库


[HiPlot](https://github.com/facebookresearch/hiplot) 
HiPlot is a lightweight interactive visualization tool to help AI researchers discover correlations and patterns in high-dimensional data using parallel plots and other graphical ways to represent information.

[Cozette](https://github.com/slavfox/Cozette)
A bitmap programming font optimized for coziness.

[matchering](https://github.com/sergree/matchering)
Open Source Audio Matching and Mastering.

[ursina](https://github.com/pokepetter/ursina)
A game engine powered by python and panda3d. 

[PyMatting](https://github.com/pymatting/pymatting)
A Python Library for Alpha Matting.

[Docket](https://github.com/keva161/Docket)
A fully fledged todo app built for test automation practice.

[dogelang](https://pyos.github.io/dg/)
A programming language that compiles to CPython bytecode, much like Scala compiles to JVM's. That essentially means that dg is an alternative syntax for Python 3. It allows you to use all of the existing libraries, too.

[pycharm-security](https://github.com/tonybaloney/pycharm-security)
A PyCharm plugin to find security holes in your Python projects.

[ldapper](https://github.com/UMIACS/ldapper)
A simple, ergonomic Python ORM for interacting with LDAP.

**[Diagrams](https://github.com/mingrammer/diagrams)**
`Diarams`作为原型化云系统架构的代码。



## 活动和网络研讨会日程


[Getting Started Testing with pytest - Boston, MA](https://www.meetup.com/bostonpython/events/266720542/)
Do you want to learn how to write automated tests in Python with pytest? We'll start from the very the very beginning! See how pytest works, and how to write tests. Once the basics are covered, we'll get into fixtures, parameterization, and coverage measurement. Then we'll do a few more advanced topics: including test doubles (mocks and fakes).

[San Diego Python Meetup February 2020 - San Diego, CA](https://www.meetup.com/pythonsd/events/xrtzkrybcdbkc/)
There will be following talks

- Python2 End of Life
- Exploring Transformers with ALBERT and BERT
- Teachable Assistant that "Knows Your Business"


[DC Python Meetup February 2020 - Arlington, VA](https://www.meetup.com/dcpython/events/267989837/)
There will be a talk, Visual Diagnostics for Machine Learning with Python.

[Hobby Robotics with Nvidia Jetson Nano - Ottawa, ON](https://www.meetup.com/ottawapython/events/xwbgcqybcdbkc/)
Gerhard Roth will cover what can be done with small robots as a hobby and will focus on how Python is used in hobby robotics. The new Nvidia Jetson Nano single board computer and the Jetbot robot which uses Jupyter notebooks will be demonstrated. A small Jetbot will be shown in action.

[Clinical Text Processing (NLP) with Python - Pittsburgh, PA](https://www.meetup.com/Python-Pittsburgh/events/268223150/)
In this talk, we will discuss some opportunities in clinical NLP, map out fundamental NLP tasks, and tour the available resources– Python libraries and frameworks for these tasks. Many of these libraries make it extremely easy to leverage state-of-the-art NLP research for building models on clinical text.

[DragonPyMeetup February 2020 - Ljubljana, Slovenia](https://www.meetup.com/Ljubljana-Python-Group/events/268065592/)
There will be following talks

- A whirlwind tour into Python SDK for Azure Machine Learning
- Going commando in Python 

https://www.meetup.com/python-14/events/ndcfkrybcdbxb/)



Posa：

> ❤️ Happy Pythonic ;-(Posa私人无责任播报)  





----- 分割线 -----

> 如果你发现哪里翻译有误的话，请务与我联系！感谢！
>




- 首发: [pythonista-weekly~蠎周刊 ~汇集全球蠎事儿 ;-)](http://weekly.pychina.org/python-weekly/pyw-437.html)
- 改进: [issue-437.md](https://github.com/PyChina/weekly/blob/master/content/python-weekly/issue%23437.md)


