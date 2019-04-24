import threading
import time

import requests
from scrapy import Selector

url = "https://movie.douban.com/top250"
lock = threading.Lock()
page_offset = 0


def get_data(url):
    """
    获取网页原数据
    :param url: 请求地址
    :return:
    """
    global page_offset
    while page_offset <= 225:  # 如果页面见底
        params = {"start": page_offset, "filter": ""}
        with lock:  # 加上操作锁，保证公用数据安全性
            page_offset += 25
        response = requests.get(url, params=params)
        if response.status_code == requests.codes.ok:  # 检测状态码
            data = response.text  # 返回响应的文本信息
            print(f"当前解析的url是：{response.url}")
            parse_data(data)

        else:
            response.raise_for_status()  # 4xx 5xx


def parse_data(data):
    """
    解析数据
    :param data:解析元数据
    :return:
    """
    se = Selector(text=data)  # 初始化selector
    print("睡觉休息3s...")
    time.sleep(3)
    # 提取数页面数据
    base_se = se.css(".grid_view .item")
    for item in base_se:
        movie_title = "".join(item.css(".hd .title::text").extract()).replace("\xa0", "")  # 替换特殊字符
        other_title = item.css(".hd .other::text").extract_first().replace("\xa0", "")
        description = item.css(".bd>p::text").extract_first().replace("\xa0", "").strip()
        poster = item.css(".pic img").xpath("./@src").extract_first()
        point_num = item.css(".star>.rating_num::text").extract_first()
        point_people = item.css(".star").xpath("./span[last()]/text()").re(r"\d+")[0]
        print({"movie_title": movie_title,
               "other_title": other_title,
               "description": description,
               "poster": poster,
               "point_num": point_num,
               "point_people": point_people})


def main():
    """
    主函数
    :return: None
    """
    print("多线程初始化中")
    t_list = [threading.Thread(target=get_data, kwargs={"url": url}) for _ in range(4)]  # 生产线程列表
    list(map(lambda x: x.start(), t_list))
    print("线程已经全部开始工作，等待子线程结束。。。")
    list(map(lambda x: x.join(), t_list))
    print("所有抓取已经完成。")


if __name__ == "__main__":
    main()
