## Python 101: iterators,generators,coroutines

> 作者：  
> Mark McDonnell  
> 发布时间: 2019-12-28  
> 原文链接：[https://www.integralist.co.uk/posts/python-generators/](https://www.integralist.co.uk/posts/python-generators/)  
>
> 翻译:  
> Dustyposa  


在这篇文章中，我将讨论一下什么是生成器`(generators)`以及和协程`(coroutines)`作比较，但是为了了解这两个概念*（生成器和协程）*我们需要回头看一看并了解迭代器`(Iterator)`的概念。
我们最终将会讨论...
- [迭代器(Iterators)](#迭代器)
    - [为什么要使用迭代器？](#为什么使用迭代器%3F)
    - [迭代器的实现](#迭代器的实现)
    - [迭代器示例](#迭代器示例)
- [生成器(Generators)](#生成器)
    - [为什么要使用生成器？](#为什么使用生成器？)
    - [生成器的实现](#生成器的实现)
    - [生成器示例](#生成器示例)
    - [生成器表达式](#生成器表达式)
    - [嵌套生成器（例如:yield from）](#生成器嵌套（例如：yield-from）)
- [协程(Coroutines)](#协程)
    - [为什么要使用协程？](#为什么使用协程？)
    - [协程的实现](#协程的实现)
    - [协程示例](#协程示例)
    - [Asyncio: 基于生成器的协程](#Aysncio%3A-基于生成器的协程)
    - [Asyncio: 新的 async 协程](#Asyncio%3A-新的-async-协程)
    - [协程的种类](#协程的种类)
    - [其他方面](#其他方面)
    
每个章节都会引导到下一章节，所以这篇文章的最好的阅读方式就是按照默认章节的顺序。除非你已经熟悉前面的部分，更喜欢跳读。

### 摘要
---

在之后我们将讨论的所有东西的摘要如下：
- 迭代器允许你对自定义对象进行迭代
- 生成器构建于迭代器之上（它们较少了模版）。
- 生成器表达式比生成器更加简洁
- 协程就*是*生成器，但是它们的`yield`接收值。
- 协程可以暂停和重新执行（对于并发来说是非常好的）

> † think [comprehensions](https://gist.github.com/e5310d1082b0ff8307e39b71a6f9bae5).

### 迭代器
---

根据官方[`Python术语表`](https://docs.python.org/3.7/glossary.html#term-iterator)，*迭代器*是...  
> 表示数据流的对象
### 为什么使用迭代器?
迭代器是很有用的，因为它允许使用标准的`Python for-in`语法对任意自定义对象进行迭代。这就是内部列表和字典类型的工作方式，以及它们如何允许`for-in`对它们进行迭代。  
更重要的是，迭代器（我们会发现）非常节省内存，这就意味着一次只能处理一个元素。因此，你可以有一个提供无限元素的序列可迭代对象并且你会发现你的程序永远不会耗尽内存分配。

### 迭代器的实现
一个迭代器是（通常）是一个实现了`__iter__ and __next__`*'双下(dunder)'*方法，尽管`__next__`方法不需要作为定义了`__iter__`方法的对象的一部分被定义。让我澄清一下...

`'迭代器'`实际上只是一些数据的容器。这个`'容器'`，根据*[协议文档(protocol documentation)](https://docs.python.org/3.7/library/stdtypes.html#iterator.__iter__)*必须有一个`__iter__`方法，应该返回一个可迭代对象（例如：一些含有`__next__`方法的东西）。`__next__`方法会在相关数据集中向前移动。

所以，你可以设计一个同时包含`__iter__ and __next__` 方法的单类*(single class)*(就像我在下面展示的)，或者你可能想把`__next__`方法定义为单独类的一部分（这取决于你感觉的什么是对于你项目来说最好的方式）。

> 注意：[collections.abc](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Iterator)对应的`Python`文档强调了那些`Pytrhon`拥有的以及各种它们需要的方法(可以看一些[我的早期文章](https://www.integralist.co.uk/posts/python-code-design/#interfaces-protocols-and-abstract-methods)，详细讨论了`protocols + abstract classes`)其他*'协议(protocols)'*。如果你对*'双下'方法还部不熟悉，我给你推荐一篇很好的文章:[魔术方法指南](https://rszalski.github.io/magicmethods/)*

通过实现这两个方法，能使`Python`迭代一个'集合(collection)'。它不关心集合是什么，只要迭代器对象定义了`Python`知道如何去迭代的行为。

### 迭代器示例
下面是一个样例，展示了如何创建这样的对象。在这个例子中，我们通过一个字符串列表传递给类的构造函数，该类实现了允许进行`for-in`迭代数据集合的相关方法。


```python
class Foo:
    def __init__(self, collection):
        self.collection = collection
        self.index = 0
    
    def __iter__(self):
        """
        我们返回 self，所以 'iterator object'就是 Foo 类实例的本身。
        
        但是我们也可以返回一个完全不同的新的实例，只要另一个 class 在它上面定义了 __next__ 方法。
        """
        print('iter be called')
        return self
    
    def __next__(self):
        """
        这个方法处理状态并向迭代器容器通知我们目前指向的我们数据集合的位置
        """
        if self.index > len(self.collection) - 1:
            raise StopIteration
            
        value = self.collection[self.index]
        self.index += 1
        
        return value

# 我们现在可以遍历我们的自定义 Foo 类了！
for element in Foo(["a", "b", "c"]):
    print(element)
```

> 注意： 抛出 `StopIteration` 异常是正确实现一个迭代器的必要条件。

在这个示例中，我们也可以**手动**迭代我们的`Foo`类，用`iter and next`函数，就像这样：


```python
foo = Foo(list("abc"))
iterator = iter(foo)

next(iterator)  # 'a'
next(iterator)  # 'b'
next(iterator)  # 'c'
```

> 注意：`iter(foo)` 和 `foo.__iter__()`相同，而`next(iterator)` 和 `iterator.__next__()`相同——所以这些函数都是由标准库提供的基础语法糖，可以让我们的代码看起来更清爽。

这种类型的迭代器被叫做'基于类的迭代器`(class-based iterator)`'，不是唯一实现可迭代对象的方法。[生成器](https://www.integralist.co.uk/posts/python-generators/#generators)以及[生成器表达式](https://www.integralist.co.uk/posts/python-generators/#generator-expressions)(请参考以下章节)是另一些节省内存的迭代对象的方式。
我们也可以通过使用`list`方法提取所有集合，就像这样：


```python
iterator = Foo(list("abc"))
list(iterator)
```

> 注意：小心点，因为如果迭代器产生无数的元素，之后就会耗尽你应用的所有内存！

### 生成器
---
根据官方[Python文档](https://docs.python.org/3.7/library/stdtypes.html#generator-types),'生成器'提供...
> 一个简便的方式去实现可迭代协议。如果一个容器对象的`__iter__()`方法被作为一个生成器实现，它将会自动返回一个可迭代对象。
### 为什么使用生成器？
他们不仅为了创建简单的迭代器提供了很好的语法，而且可以帮助减少让一些东西可迭代所需的模版代码。

一个生成器可以帮助减少与'基于类'的迭代器相关的模版代码，因为他们可以被设计来去处理'状态管理(`state management`)'逻辑，否则你不得不自己编写。

### 生成器的实现
生成器是一个返回'生成器迭代器`(gerator iterator)`'的函数，所以它的行为和`__iter__`工作方式类似（记住它返回一个迭代器）。

实际上，生成器是迭代器的子类。生成器函数本身应该利用`yield`语句将控制权返回给生成器函数的调用方。

调用方在之后可以通过`for-in`语句或者`next`函数来推进生成器迭代器（和我们之前的'基于类'的迭代器的例子中看到的那样），这再次突出了生成器实际上是迭代器的子类。

当生成器`yields`时，它实际上在那时候暂停了函数并返回了一个值。调用`next`（或者作为`for-in`的一部分）将会推进函数，要么移动到生成器函数结束或者在生成器函数中的下一个`yield`声明处停止。

### 生成器示例
下面的例子将会先打印 `a`, 然后`b`，最后`c`：



```python
def generator():
    yield "a"
    yield "b"
    yield "c"

for v in generator():
    print(v)
```

如果我们用`next()`函数作为替代，我们可以执行如下操作：


```python
gen = generator()
next(gen)  # a
next(gen)  # b
next(gen)  # c
next(gen)  # raises StopIteration
```

注意，和我们早期自定义'基于类'迭代器相比，我们已经大大的减少了我们的代码样板，因为不需要再去在类示例上定义`__iter__ and __next__`方法（我们自己也不需要管理任何状态）。我们简单地调用`yield`。

如果我们的使用足够简单，那么生成器就够了。否则如果我们需要执行非常特殊的逻辑，可能就需要自定义'基于类'的生成器了。

记住，迭代器（以及生成器扩展）是非常节省内存的，因此我们可以创建一个生成无限多元素的生成器，就像这样：


```python
def unbouded_generator():
    while True:
        yield "some value"

gen = unbouded_generator()

next(gen)  # some value
next(gen)  # some value
next(gen)  # some value
next(gen)  # some value
next(gen)  # ...

# 译者注，我们也可以关闭或者抛出异常来结束生成器，就像这样
gen.close()
next(gen)  # StopIteration
gen.throw(ValueError("Too many balue"))  # ValueError
```

所以，就像我们之前提到的，当对生成器函数用`list()`的时候也要小心（见下面的例子），因为这将获取整个集合，可能耗尽你应用的内存。


```python
def generator():
    yield "a"
    yield "b"
    yield "c"
    
gen = generator()
list(gen)  # ['a', 'b', 'c']
```

### 生成器表达式
根据官方的[PEP 289文档](https://www.python.org/dev/peps/pep-0289/)，对于生成器表达式...
> 生成器表达式是列表推导式的一个高性能，省内存的泛化。

本质上它们是一种用与[列表推导式](https://gist.github.com/e5310d1082b0ff8307e39b71a6f9bae5)相似的语法创建生成器的方法。

以下是一个会打印`"foo"`5次的生成器函数的示例：


```python
def generator(limit):
    for i in range(limit):
        yield "foo"

for v in generator(5):
    print(v)
```

这和生成器表达式是一样的：


```python
for v in ("foo" for i in range(5)):
    print(v)
```

生成器表达式的语法也和推导式的语法很相似，不同之处在我们使用`()`替代了边界/分界符`[] or {}`。


```python
(expression for item in collection if condition)
```

> 注意： 尽管没有演示，因为支持`"if"`条件，你也可以过滤生成值。

### 生成器嵌套（例如：yield from）
Python 3.3 提供了 `yield from`语句，提供了一些基础语法糖来处理嵌套生成器。

让我们来看一下如果没有`yield from`我们需要怎么做：


```python
def baz():
    for i in range(10):
        yield i

def bar():
    for i in range(5):
        yield i

def foo():
    for v in bar():
        yield v
    for v in baz():
        yield v
        
for v in foo():
    print(v)
```

注意我们有两个单独的`for-in`循环（在`foo`生成器函数中），每个循环对应一个嵌套生成器。

现在，让我们看看用`yield from`会怎样：


```python
def baz():
    for i in range(10):
        yield i
        
def bar():
    for i in range(5):
        yield i
        
def foo():
    yield from baz()
    yield from bar()

for v in foo():
    print(v)
```

Ok 这并不是很突出的功能，但是如果你曾经对`yield from`很疑惑，你现在知道了它是`for-in`语法的简单版外观。

尽管值得指出的是，如果我们没有`yield from`，我们仍然可以使用`itertool`模块的`chain()`函数来改写我们的原代码，就像这样：


```python
from itertools import chain

def baz():
    for i in range(10):
        yield i
        
def bar():
    for i in range(5):
        yield i
        
def foo():
    for v in chain(bar(), baz()):
        yield v

for v in foo():
    print(v)
```

> 注意：请参阅[PEP 380](https://www.python.org/dev/peps/pep-0380/)以获得更多关于`yield from`的详细信息，以及将其包含在·Python·语言中的基本原理。

### 协程
---

协程（就`Python`而言）一直被设计成生成器的扩展。

> 协程是计算机程序的一类组件，推广了协作式多任务的子程序，允许执行被挂起与被恢复。—— 维基百科

### 为什么使用协程？

因为协程可以暂停和恢复执行上下文，对于并发编程来说非常合适，因为它们可以让程序决定什么时候'切换上下文'。

这就是协程为什么经常被用来处理例如：[事件循环](https://www.integralist.co.uk/posts/python-asyncio/#event-loop)(构建于`Python`的 `asyncio`之上)。

### 协程的实现
生成器用`yield`关键字在函数中在某时间点返回值，但是对于协程，`yield`指令**也**可以被用在`=`操作符的右边。表示它可以在这个时间点**接收一个值**。

### 协程示例
下面是一个协程的示例。记住！协程任然是一个生成器，所以你会看到我们的例子用了和生成器相关的特性（例如：`yield` 和 `next()`函数）：
> 注意：请参考注释来提高可读性


```python
def foo():
    """
    注意我们在传统的生成器和协程上都使用了 yield
    """
    msg = yield  # 协程特性
    yield msg  # 生成器特效

coro = foo()

# 因为一个协程是一个生成器，我们需要驱动返回的生成器到达生成器函数中的第一个 yield
next(coro)

# .send() 语法对于生成器来说是很特别的，这一句代表了向第一个yield 发送了 "bar"
# msg 变量将被分配这个值
result = coro.send("bar")

# 因为我们的协程也产生了 msg 变量
# 这意味着我们可以打印值
print(result)  # bar
```

> 注意：`coro`是一个标识符，通常指代一个协程。要查看其他更多的协程可以用的方法，请查看[文档](https://docs.python.org/3.8/reference/datamodel.html#coroutines)。

下面是用协程使用`yield`在调用方通过`.send()`方法接收值之前向调用者返回了一个值。


```python
def foo():
    msg = yield "beep"
    yield msg
    
coro = foo()

print(next(coro))  # beep

result = coro.send("bar")

print(result)  # bar
```

你可以看到上面的例子，当我们移动生成器协程到一个`first`语句(使用`next(coro`)时，值`"beep"`被返回给我们用来`print`了。

### Aysncio: 基于生成器的协程
当`asyncio`模块首次被推出时，它还不支持`async/await`语法，因此当它被引入时，为了确保任何有需要被并发运行的遗留代码(例如: `awaited`)都需要使用一个`asyncio.coroutine`装饰器函数，来让它和新的`async/await`语法保持兼容。

> 注意：有关这个被弃用的特性（从 `Python` 3.10开始） ，以及一些其他适用于基于协程的生成器函数，比如`asyncio.iscoroutine`的信息，请参考文档。

最初基于生成器的协程意味着任何基于`asyncio`的代码都需要使用`yield from`在`Futures`以及另外协程上等待。

下面的示例演示了如何同时使用新的`async`协程和早期的基于生成器的协程：


```python
import asyncio

@asyncio.coroutine
def old_style_coroutine():
    yield from asyncio.sleep(1)
    
async def main():
    await old_style_coroutine()
```

### Asyncio: 新的 async 协程

使用`async def`创建的协程是用的最新的`__await__`双下方法（[文档在这里](https://docs.python.org/3.8/reference/datamodel.html#coroutines)）,然而基于生成器的协程使用了传统的基于'生成器'的实现。

### 协程的种类

这导致了术语'协程'在不同的语境下有不同的含义。我们现在有：
- `simple coroutines`：传统的生成器协程（非 async io）
- `generator coroutine`: 用传统的 `asyncio`实现的 async io
- `native coroutines`：用最新的 `async/await`实现的async io

### 其他方面

`Python`提供的一些有趣的装饰器函数可能有一些让人迷惑，因为这些函数看起来有重叠的功能。

它们并不重叠，但似乎是一起使用的：
- `types.coroutine`: 将生成器函数转为一个协程
- `asyncio.coroutine`: 确保`asyncio`兼容性的抽象

> 注意：之后我们会看到，`asyncio.coroutine`实际上调用了`types.coroutine`。在处理`asyncio`代码时，你最好使用前者。

更具体的来说，如果我们看一下[`asyncio.coroutine`](https://github.com/python/cpython/blob/master/Lib/asyncio/coroutines.py#L105)代码的实现，我们可以看到：
 1. 如果被装饰的函数已经是一个协程了，那么就直接返回。
 2. 如果被装饰的函数是一个生成器，那么就将它转为协程(使用`types.coroutine`)。
 3. 否则装饰被装饰的函数，以便当它被转为协程时，它可以`await`任何可以等待的结果。
 
