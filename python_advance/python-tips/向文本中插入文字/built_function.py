import fileinput
from typing import Iterable


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


def read_all_text(files: Iterable) -> None:
    """
    读取所有文件数据
    :param files: 数据组
    :return:
    """
    with fileinput.input(files=files) as f:
        for line in f:
            print(line, end="")


if __name__ == '__main__':
    # read_all_text(["a.txt", "b.txt"])
    replace_file_data("b.txt", "add data")
