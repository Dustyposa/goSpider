import csv
import random
import re
import time
from datetime import date, datetime, timedelta
from typing import Set, List, Tuple, Sequence, Dict, Any, Generator
import itertools

import requests
from scrapy import Selector

from spider_project.asynchronous.qiutan.config import CATCH_LIST, COMPANY_LIST, CSV_FILED, DELAY_TIME
from spider_project.asynchronous.qiutan.save_helper import MongoDb


def insert_if_nothingness(match, data):
    res = db.mongo_col.find_one({"catch_name": match})
    if not res:
        db.mongo_col.insert_one(data)
        print("insert success")
    print("exits!")


def get_catch_urls():
    """首页"""
    start_url = "http://zq.win007.com/jsData/infoHeader.js"
    base_url_dict = {
        "0": "http://zq.win007.com/cn/League/{}.html",
        "1": "http://zq.win007.com/cn/SubLeague/{}.html",
    }
    response_data = requests.get(start_url, headers=headers)
    response_data = response_data.text
    for match in CATCH_LIST:
        res = re.search(fr"\"(\d+),{match},(\d),(\d)", response_data)
        if not res:
            db.mongo_col.insert_one({"catch_name": match, "homepage": None})
        else:
            if res.group(2) == "1":
                if res.group(3) == "0":
                    insert_if_nothingness(match=match, data={"catch_name": match,
                                                             "homepage": base_url_dict[res.group(3)].format(
                                                                 res.group(1))})
                else:
                    insert_if_nothingness(match=match, data={"catch_name": match,
                                                             "homepage": base_url_dict[res.group(3)].format(
                                                                 res.group(1))})


def get_all_catch_detail():
    r = db.mongo_col.find()
    sub_sclass_pattern = re.compile(r"var SclassID = (\d+);var SubSclassID = (\d+);")
    catch_detail_params = {
        "matchSeason": f'{years}-{years + 1}',
        "round": 1,
    }
    for data in r:
        # if data[str(years)].get("catch_set"):
        if data.get(str(years)):
            if len(data) > 3 and len(data[str(years)].get("catch_set", 0)) != 0:
                continue
        url = data.get("homepage")
        if not url:
            continue
        _id = data["_id"]
        print(f"正在抓取:{url}")
        response = requests.get(url, headers=headers)
        print(f"获取数据成功")
        response.raise_for_status()
        response = response.content.decode("u8")
        rs = re.search(sub_sclass_pattern, response)
        assert rs is not None, f"search subsclass failed!\nresponse:{response}\nrs:{rs}"
        s_class_id, subs_class_id = rs.groups()
        if s_class_id == "273":
            subs_class_id = handle_australia_sclassid(s_class_id, subs_class_id)
        catch_detail_params.update(
            sclassId=s_class_id,
            subSclassId=subs_class_id,
            flesh=random.random()
        )
        response_set = set()
        get_all_catch_oddlist(
            session=requests.Session(),
            res_set=response_set,
            params=catch_detail_params,
            headers=headers
        )
        if response_set:
            db.mongo_col.update_one({"_id": _id}, {"$set": {str(years): {"catch_set": list(response_set)}}})
        time.sleep(DELAY_TIME)


def get_all_catch_oddlist(session, res_set, params, headers):
    """获取一年的所有比赛, 向集合中添加数据"""
    catch_detail_url = "http://zq.win007.com/League/LeagueOddsAjax"
    init_page = 1
    res_set_pattern = re.compile(r"\d+")
    params.update(round=str(init_page))
    res = session.get(catch_detail_url, params=params, headers=headers)
    print(res.url)
    res.raise_for_status()
    r_list = res.text.split(";")
    if len(r_list) == 2:
        params.update(matchSeason=years)
        res = session.get(catch_detail_url, params=params, headers=headers)
        r_list = res.text.split(";")
    if len(r_list) == 2:
        sub_sclass_id = handle_australia_sclassid(params.get("sclassId"), params.get("subSclassId"))
        params.update(subSclassId=sub_sclass_id)
        res = session.get(catch_detail_url, params=params, headers=headers)
        r_list = res.text.split(";")
    while len(r_list) > 2:
        for data in r_list[:-2:3]:
            re_res = res_set_pattern.search(data)
            if re_res:
                res_set.add(re_res.group())
        print(f"page {init_page} crawled over\n{r_list}")
        init_page += 1
        params.update(round=str(init_page), flesh=random.random())
        time.sleep(DELAY_TIME)
        print(catch_detail_url)
        res = session.get(catch_detail_url, params=params, headers=headers)
        # res.raise_for_status()
        r_list = res.text.split(";")
    print("已获取国家一年的所有比赛")


# def get_odds_company_data(mach_id: str) -> List[Tuple[str, str]]:
#     res_data = []
#     base_url = f"http://1x2d.win007.com/{mach_id}.js"
#     score_url = f"http://op1.win007.com/oddslist/{mach_id}.htm"
#     time_scores = get_score_time(score_url, requests.Session())
#     response = requests.get(base_url, headers=headers)
#     response.raise_for_status()
#     # base_pattern = re.compile(r'var hometeam_cn="(\w+)";.*?var guestteam_cn="(\w+)";.*?var game=Array\((.*?)\);',
#     #                           re.S)  # 获得 主队客队及公司网址
#     base_pattern = re.compile(r'var hometeam_cn="(\w+)";.*?var guestteam_cn="(\w+)";.*?var game=Array\((.*?)\);',
#                               re.S)  # 获得 主队客队及公司网址
#     search_data = re.search(base_pattern, response.text)
#     home_team_name, guest_team_name, all_games = search_data.groups()
#     iter_game = all_games.strip('"').split('","')
#     for game in iter_game:
#         tmp_list = game.split("|")
#         company_name = tmp_list[-3]
#         if company_name in COMPANY_LIST:
#             data = tmp_list[1]
#             res_data.append((company_name, data))
#     return res_data


def get_check_time_dict(iter_game_detail):
    res_dict = {}
    for g_d in iter_game_detail:
        tmp_list = g_d.split("|")
        key, _ = tmp_list[0].split("^")
        v = f"{years}-{tmp_list[3]}"
        res_dict[key] = v
    return res_dict


def get_odds_data(mach_id: str) -> Sequence[Any]:
    base_url = f"http://1x2d.win007.com/{mach_id}.js"
    score_url = f"http://op1.win007.com/oddslist/{mach_id}.htm"
    catch_time, score1, score2 = get_score_time(score_url, requests.Session())
    print(f"catch_time:{catch_time},score_url:{score_url}")
    if catch_time == "no":
        return [None] * 6
    catch_time_obj = datetime.strptime(catch_time, "%Y-%m-%d %H:%M")
    time_check = timedelta(minutes=5)
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()
    base_pattern = re.compile(
        r'var hometeam_cn="(\w+)";.*?'
        r'var guestteam_cn="(\w+)";.*?'
        r'var game=Array\((.*?)\);.*?'
        r'var gameDetail=Array\((.*?)\);',
        re.S)  # 获得 主队客队及公司网址
    search_data = re.search(base_pattern, response.text)
    if not search_data:
        return [None] * 6
    home_team_name, guest_team_name, all_games, game_detail = search_data.groups()
    iter_game = all_games.strip('"').split('","')
    iter_game_detail = game_detail.strip('"').split('","')
    company_data = {}
    check_time_dict = get_check_time_dict(iter_game_detail)
    for game in iter_game:
        tmp_list = game.split("|")
        company_name = tmp_list[-3]
        if company_name in COMPANY_LIST:
            c_id, win, flat, fail = tmp_list[1], tmp_list[-14], tmp_list[-13], tmp_list[-12]  # -14, -13, -12
            check_time_obj = datetime.strptime(check_time_dict[c_id],
                                               "%Y-%m-%d %H:%M")
            if catch_time_obj - check_time_obj <= time_check:
                print(f"时间符合:{company_name}")
                company_data[company_name] = [win, flat, fail]
    return catch_time, home_team_name, guest_team_name, score1, score2, company_data


def handle_time(date_str: str):
    start, end = date_str.split("-")
    __, s_end = end.split(",", maxsplit=1)

    return ",".join([start, s_end])


def handle_australia_sclassid(sclassid: str, subsclassid: str):
    today = date.today()
    base_url: str = (f"http://zq.win007.com/jsData/matchResult/{years}-{years + 1}/"
                     f"s{sclassid}_{subsclassid}.js?version={today.strftime('%Y%m%d')}")
    res = requests.get(base_url, headers=headers)
    if res.status_code == 404:
        base_url: str = (f"http://zq.win007.com/jsData/matchResult/2019/"
                         f"s{sclassid}_{subsclassid}.js?version={today.strftime('%Y%m%d')}")
        res = requests.get(base_url, headers=headers)
        res.raise_for_status()
    pattern = re.compile(r"var arrSubLeague = \[\[(\d+),'联赛'")
    re_data = re.search(pattern, res.text)
    if not re_data:
        return sclassid
    new_sclassid = re_data.group(1)
    print("new_sclassid:", new_sclassid)
    return new_sclassid


def get_response(url, session):
    return session.get(url).text


def handle_response(data):
    se_data = Selector(text=data)
    data_list = se_data.xpath("//td").xpath("string(.)").extract()
    return data_list[9:]


def save_response(year, catch_name, data_dict):
    base_data = db.mongo_col.find_one({"catch_name": catch_name})
    _id = base_data["_id"]
    year = str(years)
    data = base_data[year]
    data["all_data"] = data_dict
    print(data)
    db.mongo_col.update_one({"_id": _id}, {"$set": {year: data}})
    print("一场比赛更新成功")


def get_match_by_db(db) -> Generator:
    for data in db.mongo_col.find():
        catch_name = data["catch_name"]
        year = str(years)
        if data.get(year):
            catch_set = data[year]["catch_set"]
            all_data = data[year].get("all_data", [])
            if not all_data:
                yield f"{years}-{years + 1}", catch_name, catch_set
            # for one_catch in catch_set:
            #     yield f"{year}-{year+1}", catch_name, one_catch


def get_once_math_odds():
    g_data = get_match_by_db(db)
    for year, catch_name, catch_set in g_data:
        data_dict = {}
        print(f"开始抓取{catch_name}")
        for one_catch in catch_set:
            data = get_odds_data(one_catch)
            time.sleep(DELAY_TIME)
            if data[0] is None:
                print(f"No.{one_catch} 抓取失败:{one_catch}")
                continue
            res = handle_res_response((year, catch_name) + data)
            res.update(odds=data[-1])
            data_dict[one_catch] = res
            print(f"No.{one_catch} 抓取成功")
        save_response(year, catch_name, data_dict)
        print(f"所有的{catch_name}已更新完毕。")


def handle_res_response(data):
    res = dict(zip(CSV_FILED, data[:-1]))
    return res


def get_score_time(url, session) -> Sequence[str]:
    response = session.get(url, headers=headers)
    pattern = re.compile(
        r'class="LName">.*?</a> ([0-9\-: ]+).*?div class="score">(\d+)</div>.*?<div class="score">(\d+)</div>', re.S)
    re_data = pattern.search(response.text)
    if not re_data:
        return ["no"] * 3
    return re_data.groups()


def get_csv():
    all_catch_data = db.mongo_col.find()
    write_to_csv(get_once_catch_data(all_catch_data))


def get_once_catch_data(all_catch_data):
    year = str(years)

    for catch in all_catch_data:
        tmp_data = catch.get(year)
        if tmp_data:
            for data in catch[year]["all_data"].values():
                yield data


def write_to_csv(data):
    file_name = f"{years}.csv"
    # odds_data = list(db.mongo_col.find_one()[str(years)]["all_data"].values())[0]["odds"]
    odds_data = ["".join(i) for i in itertools.product(COMPANY_LIST, "胜平负")]
    fields = CSV_FILED + odds_data
    # print(fields)
    print(fields)
    with open(file_name, "w", newline="", encoding="utf_8_sig") as f:
        # writer = csv.writer(f)
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        for i in data:
            res = {}
            for k, v in i.items():
                if k != "odds":
                    res[k] = v
                else:
                    for com_k, com_v in v.items():
                        res.update(zip(["".join(ck) for ck in list(itertools.product([com_k], "胜平负"))], com_v))

            writer.writerow(res)
    print("写入csv成功")


if __name__ == "__main__":
    headers = {
        "Referer": "http://zq.win007.com/info/index_cn.htm",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36}",
    }

    years = 2018
    years_list = [2019, 2018, 2017]
    db = MongoDb()
    # get_catch_urls()
    # get_all_catch_detail()  # 1
    # res = get_odds_data("1720904")
    get_once_math_odds()  # 2
    get_csv()  # 3
    # print(res)
    # save_response(1, "英超", 2)
    # db.mongo_col.update_many({}, {"$unset": {"2018": 1}})
    # db.mongo_col.update_many({}, {"$unset": {"2017": 1}})
    # for data in db.mongo_col.find():
    #     _id = data.get("_id")
    #
    #     for y in years_list:
    #         y = str(y)
    #         year_data = data.get(y)
    #         if year_data:
    #             catch_data = year_data["catch_set"]
    #             db.mongo_col.find_one_and_update({"_id": _id}, {"$set": {y: {"catch_set": catch_data}}})
