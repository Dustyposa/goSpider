Title: pythonista-weekly : Pyw 436
Date: 2020-02-15 10:26
Tags: Weekly,pythonweekly,Zh 
Slug: pyw-436

### 欢迎阅读《pythonista周刊》第436期。Let us start!


>原文: [https://mailchi.mp/pythonweekly/python-weekly-issue-436](https://mailchi.mp/pythonweekly/python-weekly-issue-436)  
>翻译：Dustyposa

**来自赞助商（PS：原文的赞助商）:**

使用 `Datadog` 监控你的python指标，日志，集群分析。使用`Datadog`的应用分析，可以深入任何纬度并且能找到你所需要的信息，来进行动态诊断和快速故障排除。[马上跟踪你的python应用吧！免费试用14天哦！](


## 文章、教程与话题


[Handling spikes of 65,000+ requests per second with Flask while managing 10% of the UK's primary schools](https://runninginproduction.com/podcast/10-scholarpack-runs-10-percent-of-the-uks-primary-schools-and-gets-huge-traffic)
In this episode of Running in Production, Gareth Thomas goes over running a platform that helps manage 3.5+ million students. There’s over 1,500 databases and it peaks at 65k requests per second. A legacy Zope server and a series of Flask microservices power it all on AWS Fargate.

[Magic: Constant-time tricks that Klaviyo uses to operate at huge scale](https://t.co/l5c5QlApa5)
Klaviyo’s data storage and processing needs are vast and have rapidly increased over time. Our external end-users and internal service consumers do not care about our data size, however, and still need rapid responses to their queries. To keep our systems running smoothly, we occasionally have to employ various unconventional optimization techniques. The specific techniques mentioned in this article are ways of taking what are normally linear or even more complex operations and making them constant time.

[5 Things You're Doing Wrong When Programming in Python](https://www.youtube.com/watch?v=fMRzuwlqfzs) ![img](https://gallery.mailchimp.com/e2e180baf855ac797ef407fc7/images/8def3887-e9e9-4a48-95e0-74045a6a23fc.png)
Python is a great language but I've seen many novices make some very fundamental mistakes and in this video I'm presenting 5 of them which cause immense pain and head scratching. I present the mistakes, their symptoms, as well as how to fix them.

[Cloudburst: Stateful Functions-as-a-Service](https://arxiv.org/pdf/2001.04592.pdf)
Function-as-a-Service (FaaS) platforms and "serverless" cloud computing are becoming increasingly popular. Current FaaS offerings are targeted at stateless functions that do minimal I/O and communication. We argue that the benefits of serverless computing can be extended to a broader range of applications and algorithms. This paper presents the design and implementation of Cloudburst, a stateful FaaS platform that provides familiar Python programming with low-latency mutable state and communication, while maintaining the autoscaling benefits of serverless computing.

[Understand Group by in Django with SQL](https://hakibenita.com/django-group-by-sql)
Understand GROUP BY in Django ORM by comparing QuerySets and SQL side by side. If SQL is where you are most comfortable, this is the Django GROUP BY tutorial for you.

[How to write a Redis Client in Python, from Scratch](https://youtu.be/C5KkQUKhc_4?t=325) ![img](https://gallery.mailchimp.com/e2e180baf855ac797ef407fc7/images/8def3887-e9e9-4a48-95e0-74045a6a23fc.png)
Have you ever wondered how hard it is to write a client for Redis? In this talk, Loris Cro will show you how to inspect RESP (Redis Serialization Protocol) using Netcat (or telnet). Then he will use that information to live code a basic Python client that implements the SET and GET commands.

[Helping IT Govern the AI/ML Ecosystem](https://hubs.ly/H0mGnnr0)
Learn how Dell and Domino created a refreshingly simple approach to help companies get their data science teams and the technologies they need up and running faster, with an easy path to scale. SPONSOR

[Full text search with django and postgres](http://voorloopnul.com/blog/full-text-search-with-django-and-postgres/)
How to implement full text search in Django without using have bloated java software.

[Building an IVR System with Python, Django and Twilio](https://www.twilio.com/blog/building-interactive-voice-response-ivr-system-python-django-twilio)
IVR stands for Interactive Voice Response system. It's a way for you to communicate with your users over the phone. IVR is operated by voice and by the DTMF tones that phones produce when pressing keys on the keypad. In this tutorial you are going to build an IVR system using Python, Django and Twilio IVR.

[Robots and Generative Art and Python, oh my!](https://www.generativehut.com/post/robots-and-generative-art-and-python-oh-my)
Wouldn't it be cool if you could link up all the power of modern-day machine learning and artificial intelligence tools with the interactivity and quick feedback loops of modern software development paradigms and pipe that directly into your plotter to make art? In this post, we're going to run through how to make plotter art in Python.

[How to Add Websockets to a Django App without Extra Dependencies](https://jaydenwindle.com/writing/django-websockets-zero-dependencies/)
Now that Django 3.0 ships with ASGI support out of the box, adding Websockets to your Django app requires no extra dependencies. In this post, you'll learn how to handle Websockets with Django by extending the default ASGI application. We'll go over how to handle Websocket connections, send and receive data, and implement the business logic in a sample ASGI application.

[Understanding best-practice Python tooling by comparing popular project templates](https://t.co/OnTsVcUDAt)

[Face Tracking Nerf Turret Project](https://www.youtube.com/watch?v=cy3QToyba4s) ![img](https://gallery.mailchimp.com/e2e180baf855ac797ef407fc7/images/8def3887-e9e9-4a48-95e0-74045a6a23fc.png)

[How I found thousands of dollars for my LinkedIn friends using Python and an obscure public database](https://t.co/TIKFlBD8VP)

[Lua and Python](https://lwn.net/SubscriberLink/812122/bd245e8bd1018885/)

[TV backlight compensation](http://www.lofibucket.com/articles/tv_backlight_compensation.html)

[Contributing to CPython](https://paper.dropbox.com/doc/Contributing-to-CPython--AuCcNnGQvvrN0p0G89TMUSy1Ag-JlgnduI6kw9MJIaGPpN9G)

[Dicts are now ordered, get used to it](https://softwaremaniacs.org/blog/2020/02/05/dicts-ordered/en/)

## 有趣的项目、工具和库

[JustPy](https://justpy.io/) 
JustPy is an object-oriented, component based, high-level Python Web Framework that requires no front-end programming. With a few lines of only Python code, you can create interactive websites without any JavaScript programming.

[vidify](https://github.com/vidify/vidify)
Watch music videos in real-time for the songs playing on your device.

[DeepSpeed](https://github.com/microsoft/DeepSpeed) 
DeepSpeed is a deep learning optimization library that makes distributed training easy, efficient, and effective.

[Contextualise](https://github.com/brettkromkamp/contextualise)
Contextualise is a simple and flexible tool particularly suited for organising information-heavy projects and activities consisting of unstructured and widely diverse data and information resources.

[Shopyo](https://github.com/Abdur-rahmaanJ/shopyo)
Open inventory management and (coming soon) Point of sales (powered by python) for small shops. Towards ERP. First-timers-friendly.

[dtale](https://github.com/man-group/dtale)
Flask/React client for visualizing pandas data structures.

[mnamer](https://github.com/jkwill87/mnamer)
An intelligent and configurable command line media file organization utility.

[Gila](https://gila.readthedocs.io/en/latest/) 
Gila is a python3 configuration library based very heavily on the Viper config library for Go. It is designed to facilitate making [12Factor apps](https://12factor.net/) as easy as possible using python3.


[Diagrams](https://github.com/mingrammer/diagrams)
Diagram as Code for prototyping cloud system architectures.

## 最近更新

[Python in Visual Studio Code – February 2020 Release](https://devblogs.microsoft.com/python/python-in-visual-studio-code-february-2020-release/)
In this release we made improvements that are listed in our changelog, closing a total of 66 issues, including a much faster startup of Jupyter Notebook editor and scaling back of configuration notifications. Keep on reading to learn more!

## 活动和网络研讨会日程

[SoCal Python Meetup February 2020 - Santa Monica, CA](https://www.meetup.com/socalpython/events/268345566/)
There will be following talks

- Internet of Energy: A Pythonic way to support California electrical fire prevention efforts
- Develop a high performance communication engine in Python


[Introduction to using GPUs for Analytics - Philadelphia, PA](https://www.meetup.com/PyData-PHL/events/268253667/)
In this presentation, Randy will highlight the uses for GPUs in analytics and data science, and present selected examples using tools from the PyData ecosystem to demonstrate the types of use cases where GPUs dramatically decrease time to process data.

[Bayesian Data Science by Simulation - New York, NY](https://www.meetup.com/nyc-uads/events/268293679/)
This tutorial is an Introduction to Bayesian data science through the lens of simulation or hacker statistics. We will become familiar with many common probability distributions through i) matching them to real-world stories & ii) simulating them. We will work with joint/conditional probabilities, Bayes Theorem, prior/posterior distributions and likelihoods, while seeing their applications in real-world data analyses. We’ll see the utility of Bayesian inference in parameter estimation and comparing groups and we’ll wrap up with a dive into the wonderful world of probabilistic programming.

[Greater Hartford Python Meetup February 2020 - Hartford, CT](https://www.meetup.com/greaterhartfordpython/events/268256638/)
There will be a talk, The Data Science Dilemma: Python or R? Why Not Use Both!

[PyHou Meetup February 2020 - Houston, TX](https://www.meetup.com/python-14/events/ndcfkrybcdbxb/)



Posa：

> ❤️ Happy Pythonic ;-(Posa私人无责任播报)  





----- 分割线 -----

> 如果你发现哪里翻译有误的话，请务与我联系！感谢！
>




- 首发: [pythonista-weekly~蠎周刊 ~汇集全球蠎事儿 ;-)](http://weekly.pychina.org/python-weekly/pyw-436.html)
- 改进: [issue-436.md](https://github.com/PyChina/weekly/blob/master/content/python-weekly/issue%23436.md)


