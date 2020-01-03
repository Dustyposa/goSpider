Title: pythonista-weekly : Pyw 430
Date: 2020-01-04 15:16
Tags: Weekly,pythonweekly,Zh 
Slug: pyw-430

### 欢迎阅读《pythonista周刊》第430期。Let us start!


>原文: [https://mailchi.mp/pythonweekly/python-weekly-issue-430](https://mailchi.mp/pythonweekly/python-weekly-issue-430)  
>翻译：Dustyposa

**来自赞助商（PS：原文的赞助商）:**  
[python开发者都需要的Vettery](https://www.vettery.com/tech?utm_source=newsletter&utm_medium=pythonweekly&utm_term=tech&utm_content=grouped&utm_campaign=ad-77579)  
Vettery是一个招聘网站，它改变了人们应聘或者雇佣的方式。准备好换工作地方了吗？免费制作简历，你的薪资你说了算，现在就和顶级雇主的HR联系吧！


## 文章、教程与话题
[Making Python Programs Blazingly Fast](https://martinheinz.dev/blog/13)

`Python`厌恶者总是说他们不想使用`Python`的理由之一就是太慢了。是的，对于特定的程序（无论使用何种编程语言），快或者慢都是非常依赖编写它的开发者自身的呃技能和能力

Python haters always say, that one of reasons they don't want to use it, is that it's slow. Well, whether specific program - regardless of programming language used - is fast or slow is very much dependant on developer who wrote it and their skill and ability to write optimized and fast programs. So, let's prove some people wrong and let's see how we can improve performance of our Python programs and make them really fast!

[Numba makes Python 1000x faster!](https://www.youtube.com/watch?v=x58W9A2lnQc) ![img](https://gallery.mailchimp.com/e2e180baf855ac797ef407fc7/images/8def3887-e9e9-4a48-95e0-74045a6a23fc.png)
In this video I introduce the absolute minimum you need to know about Numba which is a just in time compiler for a subset of Python and Numpy. The first half of the video is dedicated to a basic intro and to highlighting a number of very common mistakes people make when using Numba. The remaining video presents a real world-ish simulation problem, shows up to a 1000x acceleration with Numba in both single and multithreaded cases, and concludes with a "reading list" for learning more about Numba.

[How to use Flask with gevent (uWSGI and Gunicorn editions)](https://iximiuz.com/en/posts/flask-gevent-tutorial)
Create asynchronous Flask application and run it with uWSGI or Gunicorn behind Nginx reverse proxy.

[Introduction to ASGI: Emergence of an Async Python Web Ecosystem](https://florimond.dev/blog/articles/2019/08/introduction-to-asgi-async-python-web/)
There's a lot of exciting stuff happening in the Python web development ecosystem right now — one of the main drivers of this endeavour is ASGI, the Asynchronous Standard Gateway Interface. This post is targeted at people interested in recent trends of Python web development. It takes you on a guided tour about what ASGI is and what it means for modern Python web development.

[Develop an Intuition for Severely Skewed Class Distributions](https://machinelearningmastery.com/how-to-develop-an-intuition-skewed-class-distributions/)
An imbalanced classification problem is a problem that involves predicting a class label where the distribution of class labels in the training dataset is not equal. Differences in the class distribution for an imbalanced classification problem will influence the choice of data preparation and modeling algorithms. Therefore it is critical that practitioners develop an intuition for the implications for different class distributions. In this tutorial, you will discover how to develop a practical intuition for imbalanced and highly skewed class distributions.

[Robot development with Jupyter](https://t.co/xe5GAgWia4)
This post shows the available tools in the Jupyter ecosystem to build advanced visualizations in Jupyter Notebooks and standalone web apps using Voilá, and how to deploy those apps to the robotics cloud.

[Creating a Moon Animation Using NASA Images and Python](https://nicholasfarrow.com/Creating-a-Moon-Animation-Using-NASA-Images-and-Python/)
Here’s how we can create a video of the moon in just a few lines of python code!

[Automating an Insider Selling Dashboard with Python & Tableau | Part 2: Collecting Live Stock Data](https://www.youtube.com/watch?v=kEVXjrt3LfA) ![img](https://gallery.mailchimp.com/e2e180baf855ac797ef407fc7/images/8def3887-e9e9-4a48-95e0-74045a6a23fc.png)
In this part, we're using pandas datareader to collect real-time stock data for our insider trades dashboard. There are lots of good nuggets in here like using Pandas to calculate moving averages and to read html. 

[Python Dictionaries 101: A Detailed Visual Introduction](https://www.freecodecamp.org/news/python-dictionaries-detailed-visual-introduction/)

[I'm not feeling the async pressure](https://lucumr.pocoo.org/2020/1/1/async-pressure/)

[Word raking with tf-idf and Python](https://igor.mp/blog/2019/12/31/tfidf-python.html)

[Label smoothing with Keras, TensorFlow, and Deep Learning](https://www.pyimagesearch.com/2019/12/30/label-smoothing-with-keras-tensorflow-and-deep-learning/)

[Meditations on the Zen of Python](https://orbifold.xyz/zen-of-python.html)

[How to use Pandas get_dummies to Create Dummy Variables in Python](https://www.marsja.se/how-to-use-pandas-get_dummies-to-create-dummy-variables-in-python)https://stackabuse.com/working-with-redis-in-python-with-django/)

## 有趣的项目、工具和库

**[Typer](https://github.com/tiangolo/typer)**
`Typer`，可以构建出色的`CLIs`。 易于编码。 基于`Python`类型提示。

> 正在寻找合适的，瞅一瞅。

**[AI_Sudoku](https://github.com/neeru1207/AI_Sudoku)**

基于`GUI`的智能数独解题器，试着从一张图片中提取数独题并解决它。

> 数独怎么解？肉眼一看就能解。

**[klaxon](https://github.com/knowsuchagency/klaxon)**

来自`Python`的`Mac OS`通知。



**[django-simple-task](https://github.com/ericls/django-simple-task)**

用于`Django 3`的简单的后台任务。

> 新鲜的后台任务来了！

**[ffmpeg-python](https://github.com/kkroening/ffmpeg-python)**

用于`FFmpeg`的`Python`绑定函数——具有复杂的过滤支持。

> 无限调用

**[Traffic-Signal-Violation-Detection-System](https://github.com/anmspro/Traffic-Signal-Violation-Detection-System)**

使用`YOLO3 & Tkinter`及基于视频片段的计算机视觉的交通信号违章检测系统。（包括GUI）



**[pylightxl](https://github.com/PydPiper/pylightxl)**

一个轻量级、零依赖、轻量级功能的`excel`读/写的`Python`库。



**[XSS-Finder](https://github.com/haroonawanofficial/XSS-Finder)**

重量级高级跨站点脚本扫描仪。



**[Robatim](https://github.com/Sanseer/Robatim)**

`Robatim `是一个基于常见的练习曲模式的伪随机音乐生成器。

> 练习曲的春天？

## 活动和网络研讨会日程

**[Austin Python Meetup January 2020 - Austin, TX](https://www.meetup.com/austinpython/events/lgrbmqybccblb/)**

`Jupyter notebooks`非常适合用来探索，尤其是分析和可视化。然而，当用于开发一个库或者自包含代码的时候，我们可以发现我们自己会复制和粘贴到我们喜欢的文本编辑器或者`IDE`。在本次演讲中，`Leanne Fitzpatrick`将介绍`nbdev`，这是`fast.ai`开发的解决此问题优雅的解决方案。



**[CI/CD for Python on AWS - Glen Allen, VA](https://www.meetup.com/PyRVAUserGroup/events/kktcmrybccblb/)**

我们将会演示：

1. 如何为`Python`应用设置持续集成管道。
2. 如何用`Python/Boto3`在`AWS`上实现持续部署。



[PyMNtos Python Presentation Night #80 - Minneapolis, MN](https://www.meetup.com/PyMNtos-Twin-Cities-Python-User-Group/events/267385506/)

[San Francisco Python Meetup January 2020 - San Francisco, CA](https://www.meetup.com/sfpython/events/xkwxvqybccblb/)

[PyAtl Meetup January 2020 - Atlanta, GA](https://www.meetup.com/python-atlanta/events/xzzgcrybccbmb/)https://morepypy.blogspot.com/2019/12/pypy-730-released.html)

## Posa：
> ❤️ Happy Pythonic ;-(Posa私人无责任播报)  

热腾腾的协程翻译: **[异步爬虫](https://github.com/Dustyposa/goSpider/blob/master/python_advance/%E7%BF%BB%E8%AF%91%E8%AE%A1%E5%88%92/%E5%BC%82%E6%AD%A5%E7%88%AC%E8%99%AB)**

初次翻译，多多指教，发现问题请提提提出来！！谢谢各位大佬了。

----- 分割线 -----

> 如果你发现哪里翻译有误的话，请务与我联系！感谢！
>




- 首发: [pythonista-weekly~蠎周刊 ~汇集全球蠎事儿 ;-)](http://weekly.pychina.org/python-weekly/pyw-430.html)
- 改进: [issue-430.md](https://github.com/PyChina/weekly/blob/master/content/python-weekly/issue#430.md)


