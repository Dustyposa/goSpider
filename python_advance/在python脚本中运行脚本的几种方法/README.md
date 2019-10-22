# 在python脚本中运行其他脚本

## 前言

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hey，又和大家见面了。不知道大家有没有这样一个需求，已经运行了一个python脚本A，但是呢，想用这个脚本A运行其他脚本，来管理脚本并获取脚本的标准输出。比如执行bash脚本（查看进程，查看机器配置信息等），运行其他辅助脚本等（包括不限于python脚本等）。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;话不多说，我们来看看如何实现。不过在实现之前，我们需要把这个问题分类。第一类为：在python脚本中运行非python脚本。第二类为：在python脚本中运行python脚本。为什么要这样分呢？因为我们的主脚本为python，所有对于python脚本有特殊优待！那么，我们就一个类一个类的看看如何实现。

## 在python脚本中运行非python脚本

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

### 2. os.execv

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这个函数和os.system有相似点，不同运行的参数不同，并且，该函数有一个特效功能，就是代替进程！什么意思呢？我们一起来看看！

>  os.execv 为一系列函数，包括 execl execve execle....主要是能给的参数不同，不过都大同小异。

```python
zsh_file = "/bin/zsh"  # 如果没有zsh 可以替换为 bash
bash_cmd_list = ["bash", "test.sh"]

def os_exec_run() -> None:
    """替代当前进程的运行"""
    print("python 正在运行")
    time.sleep(5)
    print("python 运行完毕，执行 bash 脚本")
    os.execv(zsh_file, bash_cmd_list)  # == os.execl(zsh_file, *bash_cmd_list)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;主要参数种类变了，第一个参数为可执行文件（linux中表现为文件有x权限），后面的参数表示执行的命令。好了，我们来看看运行效果。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们同样开了两个zsh窗口，查看不同时候的进程运行状态，console 的结果就不展示了，相信大家都知道。这里我们展示在执行  `os.execv` 之前和之后的进程。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`execv`执行前的进程信息：

 ```python
  PID TTY           TIME CMD
10892 ttys001    0:00.06 /Applications/iTerm.app/Contents/MacOS/iTerm2...
10899 ttys001    0:00.54 -zsh
14607 ttys001    0:00.03 /usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/...
12085 ttys002    0:00.03 /Applications/iTerm.app/Contents/MacOS/iTerm2...
12087 ttys002    0:00.19 -zsh
 ```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们可以看到，有两个zsh进程和一个python进程，正常操作。之前说到替换进程，那我们来看看运行`bash`脚本后有什么不同(请注意我们的python进程的PID)。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`execv`执行后的进程信息：

```python
10892 ttys001    0:00.06 /Applications/iTerm.app/Contents/MacOS/iTerm2...
10899 ttys001    0:00.54 -zsh
14607 ttys001    0:00.04 bash test.sh
14617 ttys001    0:00.00 sleep 5
12085 ttys002    0:00.03 /Applications/iTerm.app/Contents/MacOS/iTerm2...
12087 ttys002    0:00.22 -zsh
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`sleep 5` 的进程还在，但是`python`进程不见了！！！！！！我们再来看看PID,注意到了吗？之前`python`进程用的PID现在变成了我们的`bash`脚本进程，`python`进程直接被替代了！没错，这就是`execv`的神奇之处。好了，神奇归神奇。那么，有什么独特的用呢！！这才是关键。那我们就介绍一种常用场景，重启`python`程序，也就是常见的`restart`功能。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们先写一段简单的脚本来进行测试该功能，取名是件难事，就随便取一个，`restart,py`:

```python
import os
import sys
import time


def run(select_data: str) -> None:
    if select_data == "a":
        print("程序休眠1s")
        time.sleep(1)
    elif select_data == "b":
        print("程序即将重启") 
        os.execv(sys.executable, ["python3"] + sys.argv)  # 或者 ["python3", __file__] 
    elif select_data == "c":
        print("程序即将退出")
        sys.exit(0)


if __name__ == '__main__':
    print("程序启动了！")
    print("请选择功能：", "A. sleep 1 s", "B. 重启程序", "C. 结束程序", sep="\n")
    while True:
        select = input("请选择：").lower()
        run(select)

```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;程序很简单，大家一看就懂，我们先运行一下看看效果。

```
$ python3 restart.py
程序启动了！
请选择功能：
A. sleep 1 s
B. 重启程序
C. 结束程序
请选择：>>> a
程序休眠1s
请选择：>>> b
程序即将重启
程序启动了！
请选择功能：
A. sleep 1 s
B. 重启程序
C. 结束程序
请选择：>>> c
程序即将退出
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;重启成功！就是这么顺畅！如果我们编写桌面软件，那么重启是必不可少的功能吧！依照这个特性，我们还能不断地换python脚本（emm。。我就是臆想一下。。用自己的手玩出新花样吧！）

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;当然，你对代码也会有疑问，我们简单解释一下：首先是`sys.executable`，返回的是当前python解释器的文件路径（也就是我们需要的可执行文件）。其次`sys.argv`返回的是一个列表，包括了执行`python xxx xx x`除python意外以外的所有参数，在这里我们就只有一个参数了(`restart.py`, 所以在这里我们也可以用`__file__`进行替代)。

> **额外注意要点：**
>
> 如果你是这样执行脚本的：
>
> `./restart.py`
>
> 可以使用`os.execv(__file__, sys.argv)`来运行该脚本。
>
> 如果你是`python restart.py`那么就跟我们演示代码的方法一致即可。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;是不是很神奇，重启替换进程，一气呵成，pid也不会改变。但是，还有一种情况，我们需要管理脚本的话，使用这两种方法是不太好实现的。所以，我们继续介绍后面的高级操作，**子进程管理**。这部分东西比较多了，我们也不会一一讲述，只做抛砖引玉，先介绍一个简单的：`os.popen`

### 3. os.popen

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`os.popen`主要就是实现对一个子进程的管理，我们可以捕获子进程的标准输出（stdou），不同于`os.system`，如果我们不主动捕获stdout,那么子进程的输出我们在主进程是看不到的，同样，我们先编写一个简单的示例：

```python
def os_popen_run() -> None:
    """使用os.popen 运行子进程"""
    print("Start")
    # bash_cmd = "zsh test.sh"
    with os.popen(bash_cmd) as pipe:  
        for line in pipe.readlines():
            print(line, end="")
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过查看源码我们可以看出，默认情况下，`os.popen`的`mode`参数为r，与文件操作的`r`类似，可读；`os.popen`返回的是一个新的对象，该对象有一个`close`用于关闭管道及进程，及`io.TextIOWrapper`对象的所有方法。主要是读操作相关方法。然后我们用 `readlines`进行等待，获取该进程所有的`stdout`并打印输出。输出结果如下：

```
Start
# 阻塞5s后出现的下面的输出
bash run start
total 56
-rw-r--r--@ 1 dustyposa  staff  11213 Oct 20 15:33 README.md
-rw-r--r--@ 1 dustyposa  staff     29 Oct 20 14:57 check_alive.py
-rw-r--r--@ 1 dustyposa  staff    630 Oct 17 21:56 restart.py
-rw-r--r--@ 1 dustyposa  staff    788 Oct 20 15:33 run_bash.py
-rw-r--r--@ 1 dustyposa  staff     67 Oct 20 15:14 test.sh
sleep over
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这样我们针对输出就能进行处理啦，比如重定向，数据清理之类。简单的，我们直接利用`print`进行重定向：

```python
# 简单修改一下代码
    with os.popen(bash_cmd) as pipe, open("bash_out.txt", "w", encoding="u8") as fp:
        for line in pipe.readlines():
            print(line, end="", file=fp)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`bash_out.txt`就生成啦！数据当然和我们上面的输出结果一致。这样我们就能将输出结果保存到某些地方了！

> 简单介绍一下其他功能：
>
> - `close`方法
>   - 关闭标准输出的管道以及结束子进程并返回结束状态码，如果返回值为None的话，说明子进程正常退出，其余为异常退出（-N表示在POSIX中表示被信号N中断）。
>
> - read，readline，seek，同文件操作
> - flush 缓存刷新
> - fillno 返回文件描述符
> - isatty 如果流是交互式的（即连接到终端/ tty设备），则返回True。
>
> 实例化对象时，还有mode参数可以为w，和文件操作类似，就是写模式，

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;到这里，我们就可以控制标准输出了，但是，我们好像还不能控制子进程，比如：如何杀死子进程，如何给子进程发送信号，子如何检查子进程状态等。那怎么办呢？不急，我们看看`os.popen`的源码，其中有一段：

```python
    if mode == "r":
        proc = subprocess.Popen(cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                bufsize=buffering)
        return _wrap_close(io.TextIOWrapper(proc.stdout), proc)
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;看一看函数名和参数，没错， `subprocess.Popen`就是我们的秘诀！

### 4. subprocess.Popen



> 参考资料  
> https://stackoverflow.com/questions/8724557/how-to-run-a-python-script-from-another-python-script-and-get-the-returned-statu  
> https://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-arguments  
> https://docs.python.org/zh-cn/3/library/asyncio-subprocess.html?highlight=subprocess#asyncio.asyncio.subprocess.Process.returncode  
>
> **os.execv:**
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
