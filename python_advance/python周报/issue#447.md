Title: pythonista-weekly : Pyw 447
Date: 2020-05-02 14:22
Tags: Weekly,pythonweekly,Zh 
Slug: pyw-447

### 欢迎阅读《pythonista周刊》第447期。Let us start!


>原文: [https://mailchi.mp/pythonweekly/python-weekly-issue-447](https://mailchi.mp/pythonweekly/python-weekly-issue-447)  
>翻译：Dustyposa

**来自赞助商（PS：原文的赞助商）:**

[python开发者都需要的Vettery](https://www.vettery.com/tech?utm_source=newsletter&utm_medium=pythonweekly&utm_term=tech&utm_content=grouped&utm_campaign=ad-77579)  
Vettery是一个招聘网站，它改变了人们应聘或者雇佣的方式。准备好换工作地方了吗？免费制作简历，你的薪资你说了算，现在就和顶级雇主的HR联系吧！

### 新鲜事

[为 Steering Council Q&A 收集问题](https://discuss.python.org/t/collecting-questions-for-a-steering-council-q-a/4010)
作为 `PyCon US 2020` 的一部分，他们计划与 `Steering Council` 进行 `Q&A` 记录。如果你有任何问题，请务必提交它们。

### 文章、教程与话题


[TCP Reset Attack 是如何做的？](https://robertheaton.com/2020/04/27/how-does-a-tcp-reset-attack-work/)
`TCP` 重置攻击是使用不超过几字节大小的单个数据包进行的。一个由攻击者精心制作并发送的欺骗 `TCP` 段，欺骗两个受害者放弃 `TCP` 连接，中断了它们之间可能重要的通信。在这篇文章中：将学习到 `TCP` 协议的基础知识，学习攻击原理，并使用一个简单的 `Python` 脚本来攻击我们自己。

[More Python for Beginners](https://www.youtube.com/playlist?list=PLlrxD0HtieHiXd-nEby-TMCoUNwhbLUnj) ![img](https://mcusercontent.com/e2e180baf855ac797ef407fc7/images/af76283a-6e65-436c-967a-900427cf6399.png)
来自 `Microsoft` 的另一种 `Python` 教程。

[在 `Rust` 代码中编写 Python 代码 — Part 2](https://blog.m-ou.se/writing-python-inside-rust-2/)
在这章中，我们将扩展我们的 `python!{}-macro` ，让其能够在 `Python` 代码中无缝使用 `Rust` 变量。我们构思了几种方式，并实现了两种。

[Hacking Together an E-ink Dashboard](https://healeycodes.com/hacking-together-an-e-ink-dashboard/)
一个树莓派仪表盘原型，省得我和智能助手说话。

[Talko: 一个端到端的聊天应用](https://t.co/WLdF2Cmcnr)
如何不用任何库或者框架构建一个完整的聊天应用。

[Python 3.9 中你应该知道的新特性](https://martinheinz.dev/blog/21) 
`Python 3.9 Beat` 就将发布了，所以是时候来看看将要推出的功能了，比如新的字典操作，新的 `functools` 以及其他～

[在 Python 应用中配置使用的最佳实践](https://tech.preferred.jp/en/blog/working-with-configuration-in-python/)
许多计算机应用可以被配置成某种的行为方式，不论是通过命令行标志，环境变量或者是配置文件。对你来说，作为一个软件开发者，处理并配置会遇到一些挑战，比如解析不可信的输入，验证输入以及在程序的各层中访问它。用 `Python` 作为一个例子，这篇文章分享了一些最佳实践，来帮助你安全并高效的处理配置。

[Simple Django deployment: a guide](https://mattsegal.dev/simple-django-deployment.html)
How to deploy Django in many small steps.

[How To Create a URL Shortener with Django and GraphQL](https://www.digitalocean.com/community/tutorials/how-to-create-a-url-shortener-with-django-and-graphql)
In this tutorial you will create a backend for a URL shortener—a service that takes any URL and generates a shorter, more readable version—while diving into GraphQL concepts, like queries and mutations, and tools, like the GraphiQL interface.

[Deep Neural Network from Scratch in Python](https://www.youtube.com/watch?v=b_w4eEiogaE) ![img](https://mcusercontent.com/e2e180baf855ac797ef407fc7/images/af76283a-6e65-436c-967a-900427cf6399.png)
Making sure a flexible neural network architecture API isn't too difficult. However, we need to be careful about the layer of abstraction we put in place in order to facilitate the work of the user who want to simply fit and predict. Here we make use of the following three concept: Network, Layer and Neuron. These three components will be composed together to make a fully connected feedforward neural network neural network.

[Use Google Sheets, S3, and Python to Build a Website Quickly](https://t.co/kvkzPGbkeV)
A survival guide for non-web developers.

[Generators, Iterables, Iterators in Python: When and Where](https://www.pythonforthelab.com/blog/generators-iterables-iterators-python-when-and-where/)
Learn how to extend your code to make it easy to loop through the elements of your classes or to generate data on the fly.

[GraphQL Tutorial with Django (Python) and Excel](https://www.youtube.com/watch?v=nPQE5B51DQ8) ![img](https://mcusercontent.com/e2e180baf855ac797ef407fc7/images/af76283a-6e65-436c-967a-900427cf6399.png)
In this Django, Excel and GraphQL Tutorial  learn how to build a GraphQL Client and Server with Django and import excel data. We will code everything from scratch.

[41 Questions to Test your Knowledge of Python Strings](https://t.co/HkQ4FbffhD)
How to crush algorithm questions by mastering string fundamentals.

[Creating Interactive Views in Django](https://hackersandslackers.com/creating-django-views/) 
Create interactive user experiences by writing Django views to handle dynamic content, submitting forms, and interacting with data.

[Monitor Your Flask Web Application Automatically With Flask-Monitoring-Dashboard](https://t.co/mUQTNhMNaG)
A tutorial on how to use and set up a simple Flask application that uses Flask-Monitoring-Dashboard to monitor the system. It will show how simple it is to get started to automatically monitor your web service and explain some of the features that Flask-Monitoring-Dashboard offers.

[Working with warnings in Python (Or: When is an exception not an exception?)](https://lerner.co.il/2020/04/27/working-with-warnings-in-python/)
How are warnings different from Python exceptions? Learn how to send and filter warnings, and why you would want to do so.

[Building a Dashboard from Scratch in 30 Minutes!](https://www.youtube.com/watch?v=SnzwO4vEkJE) ![img](https://mcusercontent.com/e2e180baf855ac797ef407fc7/images/af76283a-6e65-436c-967a-900427cf6399.png)
How to build Insider Selling Dashboard entirely from scratch in 30 minutes.

[PyTorch Distributed Training](https://leimao.github.io/blog/PyTorch-Distributed-Training/)
This post presents a simple implementation of PyTorch distributed training on CIFAR-10 classification using DistributedDataParallel wrapped ResNet models. The usage of Docker container for distributed training and how to start distributed training using torch.distributed.launch would also be covered.

[Create Your Own Diff-Tool Using Python](https://florian-dahlitz.de/blog/create-your-own-diff-tool-using-python)
In this article you will learn how to create your own diff-tool using nothing but Python.

[Coding a Python Stock Trading bot with Alpaca](https://www.youtube.com/watch?v=9R7pCh4yCm8) ![img](https://mcusercontent.com/e2e180baf855ac797ef407fc7/images/af76283a-6e65-436c-967a-900427cf6399.png)

[Oops! Removing Secrets from Django Project in Docker](https://startcodingnow.com/removing-secrets-from-django-project-in-docker)

[Introducing django-gsheets, an easy way to sync to and from Google Sheets](https://labs.meanpug.com/sync-data-to-and-from-google-sheets-with-django-gsheets)

[Jupyter Notebook Best Practices](https://levelup.gitconnected.com/jupyter-notebook-best-practices-fc326eb5cd22)



### 书籍

[Springer releases 50 Programming books for free](https://link.springer.com/search/page/1?facet-discipline="Computer+Science"&package=mat-covid19_textbooks&facet-language="En"&facet-content-type="Book")
It includes books on Python, Machine Learning, Deep Learning, AI and more.

### 有趣的项目、工具和库


[Shynet](https://github.com/milesmcc/shynet)
Modern, privacy-friendly, and detailed web analytics that works without cookies or JS.

[Jina](https://github.com/jina-ai/jina) 
Jina is the cloud-native neural search framework powered by state-of-the-art AI and deep learning.

[pivotnacci](https://github.com/blackarrowsec/pivotnacci)
A tool to make socks connections through HTTP agents.

[ESPnet](https://github.com/espnet/espnet)
End-to-End Speech Processing Toolkit.

[Printy](https://github.com/edraobdu/printy)
Printy is lite and cross-platform library that extends the functionalities of the built-in functions print() and input(). Printy stands out for its simplicity and for being and easy to use library, it lets you colorize and apply some standard formats to your text with an intuitive and friendly API based on flags.

[RepoPeek](https://github.com/sameera-madushan/RepoPeek)
Python script to get details about a repository just from your terminal before cloning it.

[shhh](https://github.com/smallwat3r/shhh)
Keep secrets out of emails or chat logs, share them using secure links with passphrase and expiration dates.

[drf-starter-template](https://github.com/nishantwrp/drf-starter-template)
An easy to use project template for small projects using Django Rest Framework.

[StockInsider](https://github.com/charlesdong1991/StockInsider)
A Python tool to collect, analyze and visualize trading indicators for stocks.

[gitland](https://github.com/programical/gitland)
A multiplayer game controlled using GitHub.

[django-sockpuppet](https://github.com/jonathan-s/django-sockpuppet)
Build reactive applications with the django tooling you already know and love. 

[BentoML](https://github.com/bentoml/BentoML) 
BentoML is an open-source platform for high-performance ML model serving.

[Taichi](https://github.com/taichi-dev/taichi) 
Productive programming language for portable, high-performance, sparse & differentiable computing.

[PyDP](https://github.com/OpenMined/PyDP) 
PyDP is a Python wrapper for Google's Differential Privacy project. The library provides a set of e-differentially private algorithms, which can be used to produce aggregate statistics over numeric data sets containing private or sensitive information.

[postgres_restorer](https://github.com/pyux/postgres_restorer)
Simple tool for restoring database during integration tests.

### 最近更新

[Python 3.9.0a6](https://mail.python.org/archives/list/python-committers@python.org/message/JJWIXYICQHCEFCJCCXVSWTP5O67UVCQC/)

### 那些活动

[Webinar: Learn Scraping with Python and Poshmark](https://my.demio.com/ref/jjUDGs9tqIYdFYiS)
In this talk, we’ll learn how to use web scraping to extract information about Poshmark listings. Then, we’ll use Python libraries to analyze and visualize the data.

#### Posa：

> ❤️ Happy Pythonic ;-(Posa私人无责任播报)  

----- 分割线 -----

> 如果你发现哪里翻译有误的话，请务与我联系！感谢！




- 首发: [pythonista-weekly~蠎周刊 ~汇集全球蠎事儿 ;-)](http://weekly.pychina.org/python-weekly/pyw-447.html)
- 改进: [issue-447.md](https://github.com/PyChina/weekly/blob/master/content/python-weekly/issue%23447.md)

