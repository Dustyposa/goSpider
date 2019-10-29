## 使用python向文本中插入文字
> 本文只记录方法，希望对你能有所帮助！

#### 第一种-原生：
主要利用文件读取和写入。
```python
def write_data_to_file(file: str, data: str) -> None:
    """
    读取文件，并将数据插入第一行
    :param file: 读取文件路径
    :param data: 插入数据
    :return:
    """
    with open(file, "r+", encoding="u8") as fp:
        tmp_data = fp.read()  # 读取所有文件, 文件太大时不用使用此方法
        fp.seek(0)  # 移动游标
        fp.write(data + "\n" + tmp_data)
```
行数很少，原理也很简单。
**如果我们要判断数据是否存在，不存在就插入，该怎么写？**
简单更改一下即可：
```python
def write_data_to_file(file: str, data: str) -> None:
    """
    读取文件，并判断每行数据，如果和要插入的数据存在，就不插入,不存在，则插入第一行。
    :param file: 读取文件路径
    :param data: 插入数据
    :return:
    """
    with open(file, "r+", encoding="u8") as fp:
        # 遍历每行数据进行判断
        for d in fp.readlines():
            if data in d:
                break  # 存在就跳出
        else:
            fp.seek(0)
            tmp_data = fp.read()  # 读取所有文件, 文件太大时不用使用此方法
            fp.seek(0)  # 移动游标
            fp.write(data + "\n" + tmp_data)
```
利用一个读取文件行做了一个判断，也比较简单。
**升级一下，在某一行进行插入。**
```python
def write_data_to_file(file: str, data: str, row: int = 1) -> None:
    """
    读取文件，在某一行插入。
    :param file: 读取文件路径
    :param data: 插入数据
    :param row: 插入行
    :return:
    """
    front_data = ""  # 前半部分存储
    after_data = ""  # 后半部分存储
    with open(file, "r+", encoding="u8") as fp:
        # 遍历每行数据进行判断行数,利用 enumerate 辅助计数
        for i, d in enumerate(fp.readlines(), start=1):
            if i >= row:
                after_data += d
            else:
                front_data += d

        fp.seek(0)  # 回到初始点
        fp.write(front_data)
        fp.write(data + "\n")
        fp.write(after_data)
```
同样代码也比较简单，利用前后分割，做的拼接。
这就是原生办法。
接下来我们介绍一个内置库`fileinput`
#### 第二种-`fileinput`实现行数据插入
使用内置的`fileinput`实现，代码更简单:
```python
def replace_file_data(file_path: str, data: str) -> None:
    """
    在第一行插入数据
    :param file_path: file 路径
    :param data: 插入的数据
    :return:
    """
    with fileinput.input(files=file_path, inplace=True) as fp:
        for d in fp:
            if fp.filelineno() == 1:
                # 如果行数为 1 则进行插入
                print(data)
            print(d, end="")
```

需要注意`inplace`必须为`true`，他会捕捉当前的`stdout`,然后加入文件，我们为了简单，就直接使用`print`，所有也可以做**删除操作**，当行数等于某行时，就不`print`即可。
我们再介绍一个小方法，数据读取，一次性读取多个文件。代码如下:
```python
def read_all_text(files: Iterable) -> None:
    """
    读取所有文件数据
    :param files: 数据组
    :return:
    """
    with fileinput.input(files=files) as f:
        for line in f:
            print(line, end="")
```
只需要调动函数即可。

`read_all_text(["a.txt", "b.txt"])`

好了，今天的小技巧就到这里，希望你能有所收获。
