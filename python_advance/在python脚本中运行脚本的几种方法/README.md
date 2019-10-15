# 在python脚本中运行其他脚本

## 前言

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hey，又和大家见面了。不知道大家有没有这样一个需求，已经运行了一个python脚本A，但是呢，想用这个脚本A运行其他脚本，来管理脚本并获取脚本的标准输出。比如执行bash脚本（查看进程，查看机器配置信息等），运行其他辅助脚本等（包括不限于python脚本等）。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;话不多说，我们来看看如何实现。不过在实现之前，我们需要把这个问题分类。第一类为：在python脚本中运行非python脚本。第二类为：在python脚本中运行python脚本。为什么要这样分呢？因为我们的主脚本为python，所有对于python脚本有特殊优待！那么，我们就一个类一个类的看看如何实现。

##在python脚本中运行非python脚本

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;首先我们用一个简单的bash脚本`test.sh`来进行测试:

```bash
ls -l  # 查看当前目录的文件及文件夹详情
sleep 5  # 休眠5s
echo "sleep over"  # 打印输出 sleep over

```

我们的目标就是在`python`脚本中运行该脚本。

直接运行脚本`bash test.sh`，输出如下：

```
total 24
-rw-r--r--@ 1 dustyposa  staff  1968 Oct 14 22:03 README.md
-rw-r--r--@ 1 dustyposa  staff   162 Oct 14 21:56 run_bash.py
-rw-r--r--@ 1 dustyposa  staff    32 Oct 14 22:01 test.sh
sleep over
```

### 1. os.system

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;该函数比较直接，`system`中的参数就作为cmd命令，并开启一个子shell执行该命令，运行代码如下：

```python
bash_cmd = "bash test.sh"


def system_run() -> None:
    """os.system 运行"""
    print("os.system start!")
    os.system(bash_cmd)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;运行函数后，结果如下：

```
os.system start!
total 24
-rw-r--r--@ 1 dustyposa  staff  1968 Oct 14 22:03 README.md
-rw-r--r--@ 1 dustyposa  staff   162 Oct 14 21:56 run_bash.py
-rw-r--r--@ 1 dustyposa  staff    32 Oct 14 22:01 test.sh
sleep over
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们可以看到，打印输出的结果在也出现在了我们运行的python脚本中（当然，你可能这是理所当然的，实际并不如此，其实这里os.system帮我们做了输出重定向，将bash脚本的stdout，重定向当前运行python脚本的进程的stdout了，可能比较复杂，后面的例子中我们会讲解）。

让我们看看进程有什么变化，运行python脚本前的进程信息(...省略了完整信息)：

```
# ps  这里只有我们开的两个zsh（shell窗口的一种，运行该命令打开的窗口）窗口
  PID TTY           TIME CMD
 5230 ttys000    0:00.03 /Applications/iTerm.app...
 5232 ttys000    0:00.21 -zsh
 5056 ttys001    0:00.03 /Applications/iTerm.app...
 5058 ttys001    0:00.63 -zsh
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;运行python脚本后的进程信息：

```
# python3 run_bash.sh 在其中一个shell运行脚本，另一个查看进程信息 
  PID TTY           TIME CMD
 5230 ttys000    0:00.03 /Applications/iTerm.app...
 5232 ttys000    0:00.36 -zsh
 5056 ttys001    0:00.03 /Applications/iTerm.app...
 5058 ttys001    0:00.76 -zsh
 5602 ttys001    0:00.03 /usr/local/Cellar/python/3.7.3...
 5603 ttys001    0:00.00 bash test.sh
 5605 ttys001    0:00.00 sleep 5
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们可以看到除了一个python脚本的进程，还有一个子shell脚本的进程同时还有一个sleep 5的进程（这个很明显是bash脚本中的命令，看来sleep 是单独运行一个阻塞进程）。在这里我们也可以思考一下刚才的输出重定向问题，我们这里有两个进程，为什么在bash进程中的输出在python进程中也能看到，而我们运行两个python进程A和B，正常情况下在A中只能看到A的输出，在B中只能看到B的输出？（是不是有点感觉了）



> 参考资料  
> https://stackoverflow.com/questions/8724557/how-to-run-a-python-script-from-another-python-script-and-get-the-returned-statu  
> https://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-arguments  
> https://docs.python.org/zh-cn/3/library/asyncio-subprocess.html?highlight=subprocess#asyncio.asyncio.subprocess.Process.returncode  
>
> os.execv:
>
> https://docs.python.org/zh-cn/3/library/os.html
>
> https://blog.petrzemek.net/2014/03/23/restarting-a-python-script-within-itself/
>
> https://stackoverflow.com/questions/44075953/python-execv-and-pipe-output
>
> https://stackoverflow.com/questions/27606653/oserror-errno-8-exec-format-error/53639140#53639140
>
> https://stackoverflow.com/questions/27606653/oserror-errno-8-exec-format-error#comment43638333_27607257

os.system  
runpy  
subprocess  

os.popen

os.execv

eval

exec
