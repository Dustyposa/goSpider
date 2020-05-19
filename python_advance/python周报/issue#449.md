Title: pythonista-weekly : Pyw 449
Date: 2020-05-16 14:22
Tags: Weekly,pythonweekly,Zh 
Slug: pyw-449

### 欢迎阅读《pythonista周刊》第449期。Let us start!


>原文: [https://mailchi.mp/pythonweekly/python-weekly-issue-449](https://mail chi.mp/pythonweekly/python-weekly-issue-449)  
>翻译：Dustyposa

**来自赞助商（PS：原文的赞助商）:**
使用 `Datadog` 监控你的python指标，日志，集群分析。使用`Datadog`的应用分析，可以深入任何纬度并且能找到你所需要的信息，来进行动态诊断和快速故障排除。[来免费试用 14 天吧！](https://www.datadoghq.com/dg/apm/python-troubleshooting/?utm_source=Advertisement&utm_medium=Advertisement&utm_campaign=PythonWeekly-Troubleshooting)

### 新鲜事

[征集志愿者! Python GitHub 迁移工作小组](https://pyfound.blogspot.com/2020/05/call-for-volunteers-python-github.html)

我们正在寻找志愿者来加入一个工作小组，参与 `Python` 从 `bugs.python.org` 迁移到 `GitHub`。我们希望确保这次迁移能代表社区的需求。

[官宣一个用 Pyro 设计最佳实验的新框架](https://eng.uber.com/oed-pyro-release/)

`Uber AI` 发布了一个在 `Pyro` 的基础上的新框架，可以让实验者无缝自动优化实验设计（OED），用于模型的快速迭代。

### 文章、教程与话题

[通过在公共仓库中反编译 Python 字节码来查找机密信息](https://blog.jse.li/posts/pyc/)

缓存控制这我周围的一切，`.pyc` 文件可能会包含一些机密信息，不应该将它签入源代码控制，使用标准的 `Python .giignore`。

[Python 风格要素](https://github.com/amontalenti/elements-of-python-style)

这篇文档超越了 `PEP8`，涵盖了我认为优秀的 `Python` 风格的核心内容。它超越了仅仅是语法和模块布局的问题，而是涉及到了范式、组织和架构等领域。

[使用 Patreon API 和 Pillow 来自动创建图片](https://www.youtube.com/watch?v=RO6JxDOVwLQ) ![img](https://mcusercontent.com/e2e180baf855ac797ef407fc7/images/af76283a-6e65-436c-967a-900427cf6399.png)（52min）

在这篇教程中，我们将学习如何使用 `Patreon API` 和 `Pillow lib` 来自动创建图片。我特别用这个在我的视频末尾添加了致谢词来感谢我的支持者。这个视频将重点关注 `Patreon` 支持者，但是在下个视频，我们将看到用 `YouTube 会员` 如何使用 `YouTube API` 来做相同的事情。

[在 VS Code 中带有热加载的 Flask 调试](https://blog.theodo.com/2020/05/debug-flask-vscode/) 

学习如何为你的 `Dockerized Flask 应用` 设置一个带有热加载的强大的 `VS Code` 调试器。

[计算机视觉与深度学习的伦理应用](https://www.pyimagesearch.com/2020/05/11/an-ethical-application-of-computer-vision-and-deep-learning-identifying-child-soldiers-through-automatic-age-and-military-fatigue-detection/)

在这篇教程中，我们将学习到如何通过自动年龄识别以及军人疲劳识别应用计算机视觉，深度学习以及 `OpenCV` 来识别潜在的儿童士官。

[从 PyTorch 转到 PyTorch Lightning](https://www.youtube.com/watch?v=QHww1JH7IDU) ![img](https://mcusercontent.com/e2e180baf855ac797ef407fc7/images/af76283a-6e65-436c-967a-900427cf6399.png)（41min）

在本视频，`William Falcon` 重构了一个 `PyTorch VAE` 到 `PyTorch Lightning`。从视频就能明显看出，这是在没有预先知识的情况下重构新的 `repository` 的真实尝试。尽管如此，整个转化用了不到 `45` 分钟。

[静态代码分析的实践介绍](https://deepsource.io/blog/introduction-static-code-analysis/)

看到代码中的常见问题了吗？让我们创建一个分析器来自动检测它们。

[RSVP for the ONLY Python Web Conference (Virtual) | June 17-19, 2020](https://pythonwebconference.com/) 
Experts discuss hard web production problems. 40+ talks on Django, Plone, CI/CD, Containers, Serverless, REST APIs, microservices, etc. Join JetBrains and Six Feet Up to discuss what the future holds. SPONSOR

[利用 InnoDB 架构优化 Django 模型设计](https://t.co/GO1oixzPnO)

每个开发人员都应该了解 `InnoDB`。

[Python 中神经网络的介绍(你梭需要知道的东西)](https://www.youtube.com/watch?v=aBIGJeHRZLQ) ![img](https://mcusercontent.com/e2e180baf855ac797ef407fc7/images/af76283a-6e65-436c-967a-900427cf6399.png)（1h）

在这段视频中，我们将从一些基础开始。我们看看我们为什么使用神经网络以及它们是如何工作的。

In this video we start by walking through some of the basics. We look at why we use neural networks and how they function. We do an overview of network architecture (input layer, hidden layers, output layer). We talk a bit about how you choose how many hidden layers and neurons to have. We also look at hyperparameters like batch size, learning rate, optimizers (adam), activation functions (relu, sigmoid, softmax), and dropout.

[Effortless Concurrency with Python's concurrent.futures](https://rednafi.github.io/digressions/python/2020/04/21/python-concurrent-futures.html)
Running simple tasks concurrently with concurrent.futures.

[How To Build a Neural Network to Translate Sign Language into English](https://www.digitalocean.com/community/tutorials/how-to-build-a-neural-network-to-translate-sign-language-into-english)
In this tutorial, you’ll use computer vision to build an American Sign Language translator for your webcam. As you work through the tutorial, you’ll use OpenCV, a computer-vision library, PyTorch to build a deep neural network, and onnx to export your neural network.

[The Complete Python Course For Beginners](https://www.youtube.com/watch?v=sxTmJE4k0ho) ![img](https://mcusercontent.com/e2e180baf855ac797ef407fc7/images/af76283a-6e65-436c-967a-900427cf6399.png)
This python course is designed to take you from beginner to pro in the python language. This python course is designed to teach you everything you need to know about python. It assumes no prior knowledge and is a perfect python tutorial for beginners. 

[Remapping Python Opcodes](https://medium.com/tenable-techblog/remapping-python-opcodes-67d79586bfd5)
This post takes you step by step through how the author recovered the source code of remapped compiled Python opcodes.

[How To Use the collections Module in Python 3](https://davidmuller.github.io/posts/2020/05/08/collections-module-Python3.html)
In this tutorial, we’ll go through three classes in the collections module to help you work with tuples, dictionaries, and lists. We’ll use namedtuples to create tuples with named fields, defaultdict to concisely group information in dictionaries, and deque to efficiently add elements to either side of a list-like object.

[SQLite Databases With Python](https://www.youtube.com/watch?v=byHcYRpMgI4) ![img](https://mcusercontent.com/e2e180baf855ac797ef407fc7/images/af76283a-6e65-436c-967a-900427cf6399.png)
In this course you’ll learn the basics of using SQLite3 with Python. SQLite is a very easy to use database engine included with Python. You’ll learn how to create databases and tables, add data, sort data, create reports, pull specific data, and more. 

[How to Prototype a Web App with Django and Vue.js](https://www.sitepoint.com/web-app-prototype-django-vue/)
Learn how use Django and Vue.js to prototype a custom, responsive and reactive web application with a full-featured back office site to manage the content.

[Creating and deploying static websites using Markdown and the Python library Pelican](https://shahayush.com/2020/03/web-pelican-intro/)
Get to know how markdown and the Python library pelican can be used to create your static website without requiring HTML and CSS skills.

[Understand the Fundamentals of the K-Nearest Neighbors (KNN) Algorithm](https://heartbeat.fritz.ai/understand-the-fundamentals-of-the-k-nearest-neighbors-knn-algorithm-533dc0c2f45a)
An introduction to the famous machine learning algorithm KNN using scikit-learn.

[Plasma: A learning platform powered by Jupyter](https://blog.jupyter.org/plasma-a-learning-platform-powered-by-jupyter-1b850fcd8624)

[Deep Learning for Guitar Effect Emulation](https://teddykoker.com/2020/05/deep-learning-for-guitar-effect-emulation/)

[Under Discussion: The Performance of Python](https://www.welcometothejungle.com/en/articles/btc-performance-python)

[Using FastAPI with Django](https://www.stavros.io/posts/fastapi-with-django/)

[Patching requests HTTP hooks with custom arguments](https://seds.nl/posts/http-hooks-with-custom-arguments/)

[An HTTP server to display desktop notifications](https://julienharbulot.com/notification-server.html)

[Build a serverless Martian weather display with CircuitPython and AWS Lambda](https://aws.amazon.com/blogs/compute/build-a-serverless-martian-weather-display-with-circuitpython-and-aws-lambda/)

[Accelerating Medical Image Segmentation with NVIDIA Tensor Cores and TensorFlow 2](https://devblogs.nvidia.com/accelerating-medical-image-segmentation-tensor-cores-tensorflow-2/)

[Using Rust to Power Python Importing With oxidized_importer](https://gregoryszorc.com/blog/2020/05/10/using-rust-to-power-python-importing-with-oxidized_importer/)



### 有趣的项目、工具和库

[MicroscoPy](https://github.com/IBM/MicroscoPy)
An open-source, motorized, and modular microscope built using LEGO bricks, Arduino, Raspberry Pi and 3D printing.

[ar-cutpaste](https://github.com/cyrildiagne/ar-cutpaste)
Cut and paste your surroundings using AR.

[this-word-does-not-exist](https://github.com/turtlesoupy/this-word-does-not-exist)
This is a project allows people to train a variant of GPT-2 that makes up words, definitions and examples from scratch.

[fastpages](https://github.com/fastai/fastpages)
An easy to use blogging platform, with enhanced support for Jupyter Notebooks. It automates the process of creating blog posts via GitHub Actions, so you don’t have to fuss with conversion scripts. 

[AI-basketball-analysis](https://github.com/chonyy/AI-basketball-analysis)
An artificial intelligence application built on the concept of object detection. Analyze basketball shots by digging into the data collected from object detection.

[spycheck-linux](https://github.com/BjornRuytenberg/spycheck-linux)
Verify whether your Thunderbolt-enabled Linux system is vulnerable to the Thunderspy attacks.

[xxh](https://github.com/xxh/xxh)
Bring your favorite shell wherever you go through the ssh.

[slack-watchman](https://github.com/PaperMtn/slack-watchman)
Monitoring you Slack workspaces for sensitive information.

[open_lth](https://github.com/facebookresearch/open_lth)
A repository in preparation for open-sourcing lottery ticket hypothesis code.

[AxCell](https://github.com/paperswithcode/axcell)
Tools for extracting tables and texts from papers.

[senator-filings](https://github.com/neelsomani/senator-filings)
Scrape public filings of the buy + sell orders of U.S. senators and calculate their returns.

[timeglass](https://github.com/mountwebs/timeglass)
Simple and unobtrusive menu bar timer for macOS.

[pandas_alive](https://github.com/JackMcKew/pandas_alive)
Animated plotting extension for Pandas with Matplotlib.

[pyp](https://github.com/hauntsaninja/pyp)
Easily run Python at the shell! Magical, but never mysterious.

[sheet2api-python](https://github.com/odwyersoftware/sheet2api-python/)
Google/Excel Sheets API Python.

[DataGene](https://github.com/firmai/datagene) 
Identify How Similar Datasets Are to One Another.

[Fluent](https://github.com/breitburg/fluent)
Fluent makes it easy and fast to build beautiful mobile apps



### 最近更新

[Python in Visual Studio Code – May 2020 Release](https://devblogs.microsoft.com/python/python-in-visual-studio-code-may-2020-release/)
In this release we addressed 42 issues, and it includes the ability to browse for or enter an interpreter path on selection. You can check the full list of improvements in the changelog. 

### 那些活动

[Virtual: Wagtail Space US 2020](https://us.wagtail.space/)
We'll be holding our conference virtually this year! We are expecting to launch our Call For Proposals in a few weeks, and announce our schedule during the first week of July. Wagtail Space US will comprise talks, training, and a sprint.

[Virtual: PyData Madison Meetup May 2020](https://www.meetup.com/PyData-Madison/events/270204693/)
There will be a demo using mybinder. Mybinder allows you to take your jupyter notebooks and turn them into an environment you can run from anywhere on any machine with all of the dependancies installed.

[Virtual: Oops! I’ve Just Spent the Entire AWS Budget](https://www.meetup.com/PyData-Edinburgh/events/270582907/)
This talk charts the personal development of the speaker during development of a dashboard application for a holiday company. It includes key decisions (and mistakes) and obstacles that led to the final design. This journey started from zero knowledge of Data Science, zero knowledge of R and zero knowledge of Cloud Computing. It highlights key areas of data security and cloud architecture needed as the application moved from concept, through to prototype and then final commercial delivery.


#### Posa：

> ❤️ Happy Pythonic ;-(Posa私人无责任播报)  

----- 分割线 -----

> 如果你发现哪里翻译有误的话，请务与我联系！感谢！




- 首发: [pythonista-weekly~蠎周刊 ~汇集全球蠎事儿 ;-)](http://weekly.pychina.org/python-weekly/pyw-449.html)
- 改进: [issue-449.md](https://github.com/PyChina/weekly/blob/master/content/python-weekly/issue%23449.md)

