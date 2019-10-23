> 原文: [https://mailchi.mp/pythonweekly/python-weekly-issue-419](https://mailchi.mp/pythonweekly/python-weekly-issue-419)
> 翻译：dusty posa
### 欢迎阅读《python周刊》第419期。Let us start!
### 来自赞助商:
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019102318133438.png)使用 `Datadog` 监控你的python指标，日志，集群分析。使用`Datadog`的应用分析，可以深入任何纬度并且能找到你所需要的信息，来进行动态诊断和快速故障排除。[马上跟踪你的python应用吧！免费试用14天哦！](https://www.datadoghq.com/dg/apm/ts-python-tracing/?utm_source=Advertisement&utm_medium=Advertisement&utm_campaign=PythonWeekly-Tshirt)
## 文章、教程与话题
#### [Dropbox 是如何构建威胁检测和安全事件响应工具的。](https://blogs.dropbox.com/tech/2019/10/how-dropbox-security-builds-better-tools-for-threat-detection-and-incident-response/)
一般情况下，最常见的构建威胁检测和响应工具的方法是解耦自动化和检测部分。根据我们的经验，这会导致大量的内存溢出。在`Dropbox`中, 我们已经为我们的日志构建了一个公共的抽象底层，通过`Alertbox`、`Covenant`和`Forerunner`在安全响应周期内的不同阶段都可以使用。集成并利用强大的开源工具能使我们快速地探索我们的数据并自动警报。我们就可以专注于解决更复杂的威胁。
> 这个安全方向有点难。。。不太熟悉。。一脸懵逼状态。。
#### [Python 3.8 有什么新东西！](https://docs.python.org/3.8/whatsnew/3.8.html)
这篇文章阐述了`Python 3.8`的新特性，并和`3.7`进行比较。
> 这个就比较熟悉啦！海象运算符（都说和 go 像，但我觉得和 c 更像，你觉得呢？）、仅位置参数、`typing.TypedDict`、f 字符串打印....
#### [python的导入指南：绝对导入，相对导入 and more~](https://www.pythonforthelab.com/blog/complete-guide-to-imports-in-python-absolute-relative-and-more/)
如何规划你的代码，让导入更加干净！
> 导入也是个头痛的问题
#### [Haptic 是如何进行庞大的 python3 迁移的](https://haptik.ai/tech/how-haptik-carried-out-their-largest-python3-migration/)
这篇文章讲述了 Haptic 是如何克服 `Python 2` 代码热（无停机）迁移到 `Python 3`代码的挑战的。
> 热迁移，高级！如果有 py2 to py3 需求，推荐一读。
#### [python分治算法的终极指南](https://skerritt.blog/divide-and-conquer-algorithms/)
容易理解的分治算法的介绍！
> 分治。算法绕不开的东西。
#### [Soundcloud 推广机器人](https://www.youtube.com/watch?v=B-xvgebrB2g)
在本篇教程中，我们将介绍如何使用 python 编写一个自动在 soundcloud 上进行推广的机器人。这真的是一个很有趣的工具，因为现在在`soundcloud`上有如此多的机器人，你可能对了解和发现机器人是如何工作的并且如何使用`python`做出属于自己的`soundcloud`是很感兴趣的。
> 虽然没用过 `soundcloud` 但是应该和 `twitter`上面的机器人功能类似，也应该很有趣！
#### [Y组合器的简单本质（用python解释）](https://lptk.github.io/programming/2019/10/15/simple-essence-y-combinator.html)

Y组合器是λ演算的核心概念，它是函数式编程的形式基础。Y允许在没有定义引用的情况下定义一个递归的函数。我见过的大多数专门解释Y组合器的文章都是从给你展示Y组合器开始（它本身就很难理解），然后尝试解释它是如何工作的。我认为这样做是反的。在本文中，我们将从另一种方式开始：我将用通俗易懂的话来描述Y组合器的本质，然后在没有递归定义的情况下如何实现递归，那时候我们就能清楚的了解一般的Y组合器了。

> 计算机基础的教程来了。犹豫就会败北！

#### [复杂的瀑布流](https://sobolevn.me/2019/10/complexity-waterfall)
在本文章，我将带着你找到存在复杂性的地方并且教你如何解决。然后我们将讨论如何编写良好的简单的代码和自动化如何适应“连续重构”和“可变架构”开发风格的。
> 代码水平也是相当重要的。
#### [用python和django向AWS S3 上传文件](https://stackabuse.com/uploading-files-to-aws-s3-with-python-and-django/)

在本文，我们将探索`Django`如何处理文件上传和我们如何用存储使用及扩展该功能，以便适应于我们的需求。

> Django知识扩展

#### [使用Pandas的qcut和cut进行数据分箱](https://pbpython.com/pandas-qcut-cut.html)

`Pandas`的`qcut`和`cut`都可以用来将连续值存储到离散箱或者连续箱中。本文将解释两个命令的不同之处，并如何使用他们。

> 数据处理小知识。

#### [使用PyQtGraph进行绘图](https://www.learnpyqt.com/courses/graphics-plotting/plotting-pyqtgraph/)

在该教程中，我们将从使用`PyQtGraph`创建绘图小部件开始，然后演示使用线条颜色、线条类型、轴标签、背景色和复杂线条定制绘图。

> 窗口绘图利器！

[如何使用MongoDB和Docker构建Flask应用](https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker)

在本教程中，你将在 docker 容器中使用`Flask MongoDB和nginx`构建、打包、运行你的`to-do`网络服务。你将在`docker-compose.yml`文件中定义全部的堆栈配置，以及`Python MongoDB 和 nginx`的配置文件。`Flask`需要一个网络服务器来服务于`HTTP请求`，所以你也会使用一个叫做`Gunicorn`的`Python WSGI服务器`来服务于应用。`Nginx`充当反响代理将请求转发给`Gunicorn`进行处理。

> 这篇文章大家应该比较感兴趣，讲解了如何部署`flask`服务，`Gunicorn`网关服务器现在也比较流行了，设置比`uwsgi`简单多了，使用更方便，首推！

[为什么我的验证损失比训练损失更小](https://www.pyimagesearch.com/2019/10/14/why-is-my-validation-loss-lower-than-my-training-loss/)

在本教程中，你将学到在训练你的深度神经网络时，你的验证损失可能低于训练损失低的三个主要原因。

> 损失损失，你为什么不一样！

#### [一个安全并非极端耦合的方式反向私有化Api](https://blog.jonlu.ca/posts/safeway)

#### [Python属性访问和描述符约定](https://amir.rachum.com/blog/2019/10/16/descriptors/)

#### [由于对python的误解，数千篇科学论文可能无效](http://www.blog.pythonlibrary.org/2019/10/13/thousands-of-scientific-papers-may-be-invalid-due-to-misunderstanding-python)

#### [有关如何在 Django 应用中使用 Sentry 实时监控软件错误的分步教程](https://blog.hlab.tech/a-step-by-step-tutorial-on-how-to-monitor-software-errors-in-real-time-using-sentry-in-django-web-applications/)

#### [使用Spotify API 和PYthon分析音乐喜好](https://nvbn.github.io/2019/10/14/playlist-analysis/)



## 有趣的项目、工具和库

