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


if __name__ == '__main__':
    write_data_to_file("./a.txt", "insert one line5", 2)
