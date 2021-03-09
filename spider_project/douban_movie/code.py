import csv
import random
import time
from pprint import pprint

import requests
from parsel import Selector

fieldnames = ['poster', 'movie_name', 'director', 'movie_type', 'score', 'country', 'year']


def get_data(url):
    response = requests.get(url, headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36"})
    if response.status_code == requests.codes.ok:  # 检测状态码
        return response.text  # 返回响应的文本信息
    else:
        response.raise_for_status()


def get_time_actor(data):
    """
    获取处理后的时间和种类数据
    :param data:
    :return:
    """
    tmp_data = data.split(" / ")
    ind = 1
    for i, v in enumerate(tmp_data):
        if v[:4].isdigit():  # 判断是否为数字
            ind += 1
        else:
            break
        return tmp_data[:ind], tmp_data[ind:]


def get_page_data(url):
    data = get_data(url)  # 获取数据
    se = Selector(text=data)

    poster = se.css(".grid_view .pic img").xpath("./@src").extract()  # 获取海报
    movie_name = se.css(".grid_view .pic img").xpath("./@alt").re("\w+")  # 获取电影名
    tmp_actor_o_info = se.css(".grid_view .info .bd").xpath("./p/text()")  # 获取上映日期和种类
    actor, other_info = tmp_actor_o_info[::4], tmp_actor_o_info[1::4]
    actor, other_info = [i.get() for i in actor], [i.get() for i in other_info]
    score = se.css(".star>.rating_num::text").extract()  # 获取评分
    movie_data = {}

    for p, m, a, o, s in zip(poster, movie_name, actor, other_info, score):
        a = a.strip()
        try:
            other_info = o.strip().replace("\xa0", " ")
            if "导演:" in a:
                director, a = a[4:].split("   ")
            else:
                director, a = a, a
            director = director.strip().split("/")  # 列表
            year, country, movie_type = other_info.strip().split("/")

            movie_type = movie_type.strip().split(" ")  # 列表
            movie_data.update(
                {m: {"poster": p, "movie_name": m, "director": "/".join(director), "movie_type": "/".join(movie_type),
                     "score": s, "country": country.strip(), "year": int(year)}})
        except ValueError:
            continue
    return movie_data


def write_to_csv(dict_data):
    with open('movies.csv', 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        [writer.writerow(row_data) for row_data in dict_data.values()]


def write_csv_header():
    with open('movies.csv', 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def read_movie_data():
    to_int_data = ["year"]
    to_float_data = ["score"]
    to_list_data = ["movie_type", "director"]
    res = []
    with open('movies.csv', 'r', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in to_float_data:
                row[key] = float(row[key])
            for key in to_int_data:
                row[key] = int(row[key])
            for key in to_list_data:
                row[key] = row[key].split("/")
            res.append(row)
    print("读取数据完成！")
    return res


def recommend_movies(movies, method, value):
    if method == 1:
        # 年份
        need_value = int(value)
        need_key = "year"
    elif method == 2:
        # 得分
        need_value = float(value)
        need_key = "score"
    elif method == 3:
        # 导演
        need_value = value
        need_key = "director"
    elif method == 4:
        # 电影类型
        need_value = value
        need_key = "movie_type"
    else:
        return movies
    res = []
    for movie in movies:
        if need_key == "year" and movie[need_key] == need_value:
            res.append(movie)
        elif need_key == "score" and movie[need_key] >= need_value:
            res.append(movie)
        elif need_key == "movie_type" and need_value in movie[need_key]:
            res.append(movie)
        elif need_key == "director" and need_value in "".join(movie[need_key]):
            res.append(movie)

    if len(res) > 10:
        return random.sample(res, 10)
    return res


def run_recommend_forever(movies):
    while True:
        method = input("""请选择推荐的依据：
1. 年代
2. 评分
3. 导演
4. 种类""")
        if method in list("1234"):
            res = input("年代，评分，导演，种类或者是？")
            movies = recommend_movies(movies, int(method), res)
            if not movies:
                print("没有可推荐的电影，请换个方式！")
            else:
                print("结果如下：")
                for m in movies:
                    time.sleep(3)
                    pprint(m)
        else:
            print("不推荐，结束。")
            break


def main():
    select = input("""欢迎使用电影小程序。
支持如下功能：
1. 抓取电影数据
2. 推荐电影数据
请选择，并回车""")
    if select == "1":
        write_csv_header()
        base_url = "https://movie.douban.com/top250?start={count}&filter="
        for i in range(10):
            url = base_url.format(count=i * 25)
            print("抓取: {}".format(url))
            movie_data = get_page_data(url)
            write_to_csv(movie_data)
            time.sleep(2)
        print("电影抓取完成。")
    elif select == "2":
        movies = read_movie_data()
        if not movies:
            print("没有电影数据！")
        else:
            run_recommend_forever(movies)

    print("程序已结束。")


if __name__ == '__main__':
    main()
