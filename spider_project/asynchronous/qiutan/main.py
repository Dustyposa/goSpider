import random
import re
import time
from datetime import date
from typing import Set, List, Tuple
from itertools import starmap

import requests
from scrapy import Selector

from spider_project.asynchronous.qiutan.config import CATCH_LIST, COMPANY_LIST
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
        if len(data) > 3 and len(data[str(years)]["catch_set"]) != 0:
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
        time.sleep(3)


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
        res = session.get(catch_detail_url, params=params)
        r_list = res.text.split(";")
    while len(r_list) > 2:
        for data in r_list[:-2:3]:
            re_res = res_set_pattern.search(data)
            if re_res:
                res_set.add(re_res.group())
        print(f"page {init_page} crawled over\n{r_list}")
        init_page += 1
        params.update(round=str(init_page), flesh=random.random())
        time.sleep(1)
        res = session.get(catch_detail_url, params=params)
        res.raise_for_status()
        r_list = res.text.split(";")
    print("已获取国家一年的所有比赛")


def get_odds_data(mach_id: str) -> List[Tuple[str, str]]:
    res_data = []
    base_url = f"http://1x2d.win007.com/{mach_id}.js"
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()
    base_pattern = re.compile(r'var hometeam_cn = "(\w+)";.*?var guestteam_cn = "(\w+)";.*?var game = Array\((.*?)\);',
                              re.S)
    home_team_name, guest_team_name, all_games = base_pattern.groups()
    iter_game = starmap(lambda x: x.strip('"'), all_games.split(", "))
    for game in iter_game:
        tmp_list = game.split("|")
        company_name = tmp_list[-3]
        if company_name in COMPANY_LIST:
            data = tmp_list[1]
            res_data.append((company_name, data))
    return res_data


def handle_australia_sclassid(sclassid: str, subsclassid: str):
    today = date.today()
    base_url: str = f"http://zq.win007.com/jsData/matchResult/{years}-{years + 1}/" \
                    f"s{sclassid}_{subsclassid}.js?version={today.strftime('%Y%m%d')}"
    res = requests.get(base_url, headers=headers)
    res.raise_for_status()
    pattern = re.compile(r"var arrSubLeague = \[\[(\d+),'联赛'")
    re_data = re.search(pattern, res.text)
    if not re_data:
        return sclassid
    new_sclassid = re_data.group(1)
    return new_sclassid


def get_response(url, session):
    return session.get(url).text


def handle_response(data):
    se_data = Selector(text=data)
    data_list = se_data.xpath("//td").xpath("string(.)").extract()
    return data_list[9:]


def save_response(data):
    print(data)


def get_once_math_odds(url, session):
    data = get_response(url, session)
    handle_data = handle_response(data)
    save_response(handle_data)


if __name__ == "__main__":
    headers = {
        "Referer": "http://zq.win007.com/info/index_cn.htm",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36}",
    }

    years = 2019
    db = MongoDb()
    # get_catch_urls()
    # get_all_catch_detail()
