import json
import re
import time
import traceback
from dataclasses import dataclass
from datetime import datetime
from json.decoder import JSONDecodeError
from pathlib import Path

import requests
from parsel import Selector, css2xpath
from headers import COMMON_HEADERS
from functools import wraps


def retry(func):
    @wraps(func)  # 保留被装饰函数的元信息
    def closure(*args, **kwargs):
        for i in range(3):
            try:
                res = func(*args, **kwargs)
            except Exception:
                time.sleep(2)
                print(f"第{i + 1}次重试。")
            else:
                return res
        return {}

    return closure


# from resource.font.map import address_mapping, review_tag_mapping, shop_num_mapping


class UrlModel:
    coupon_url = "http://www.dianping.com/ajax/json/shopDynamic/promoInfo"  # 优惠促销
    ordered_url = "https://reserve.dianping.com/plusdom/poidetail"  # 预定人数
    recommend_url = "http://www.dianping.com/ajax/json/shopDynamic/allReview"  # 推荐菜
    recommend_menu_price_url = "http://www.dianping.com/ajax/json/shopDynamic/shopTabs"  # 推荐菜价格
    shop_url = "http://www.dianping.com/shop/{}"
    m_shop_url = 'https://m.dianping.com/shop/{}'
    font_css_url = "http://s3plus.meituan.net/v1/mss_{}.css"
    pre_fix = "http://"


class FontMapper:
    @staticmethod
    def map(font_list, map_type=1):
        if map_type == 1:
            map_data = ...
        elif map_type == 2:
            map_data = ...
        elif map_type == 4:
            map_data = ...
        else:
            raise NotImplementedError(f"don't know the map type: {map_type}")
        return "".join(map(lambda x: x, font_list))


class PageParser:
    def __init__(self, text: str):
        self.sel = Selector(text)


@dataclass
class CouponModel:
    name: str  # 优惠券名字
    old_price: float  # 原来的价格
    now_price: float  # 现在的价格
    saled_count: int  # 售出的数量


@dataclass
class BaseInfoSelectorXpathRules:
    comments_num_rule = css2xpath("#reviewCount .num::text")  # 评论数量
    per_capita_rule = css2xpath("#avgPriceTitle .num::text")  # 人均消费
    taste_score_rule = css2xpath("#comment_score") + "/span[contains(text(), '口味')]/d/text()"  # 口味评分
    env_score_rule = css2xpath("#comment_score") + "/span[contains(text(), '环境')]/d/text()"  # 环境评分
    service_score_rule = css2xpath("#comment_score") + "/span[contains(text(), '服务')]/d/text()"  # 服务评分
    shop_address_rule = css2xpath("#address ::text")  # 店铺地址
    open_time_rule = css2xpath(".info.info-indent>.item ::text")  # 开店时间
    other_shop_rule = css2xpath(".more-shop ::text")  # 更多店铺
    shop_phone_rule = css2xpath(".expand-info.tel ::text")  # 店铺电话
    shop_name_rule = css2xpath(".shop-name::text")  # 店铺名字


class AllMsgGenerator:
    def __init__(self, shop_id, session, params=None):
        self.res = {}
        self.shop_id = shop_id
        self.session = session
        if params:
            self.params = params
        else:
            self.params = {"shopId": self.shop_id,
                           "originUrl": f"http://www.dianping.com/shop/{self.shop_id}",
                           'shopType': 10,
                           'cityId': 8,
                           '_token': "eJxVj0FvgkAQhf/LXLuB3XUXkBvW2FADTQXWpI0HRFxIASmLoDb9713Seuhp3nzvvWTmCzr/AC7BGDOCYMg7cIEY2LAAQa+0w+eEE844sdgcQfaPUWxbCPadWIL7TiwHoxmzdxPZaPBLCOZ4h+6aanumY3hK+ToERd+3rmmO42gcyrRpy0Ya2ak2VXFqzcoprZDeuuPbpT4/0lEfBbpZx1OTMxtRzCbwMQE907/Z3/dAv6NLqpSNVvnzJY4UU5/HTaDiBAf2Ilk7coiv9BqKpLspOXh+V22fovRhU4lVKlYij7YvxVlIRyzXso/2rzisPK8qF0EG3z9nDFoO",
                           }
        self.params["shopId"] = shop_id
        self.comments_parser = CommentsParser(self.session, self.params)  # 推荐菜
        self.comments_data = self.comments_parser.get_comments_info() if self.res.get("msg") != "该商户不展示评价" else (
            0, 0, 0, 0, [])

    def get_order_num(self):
        """预定人数"""

        content = requests.get(UrlModel.ordered_url, params=self.params).content.decode("u8")
        res = re.search(r"(\d+)人已订", content)
        if res:
            return int(res.group(1))
        return 0

    def get_coupon_data(self):
        """优惠券"""
        url = UrlModel.m_shop_url.format(self.shop_id)
        # resp = requests.get(url=url, headers=COMMON_HEADERS)
        # tags = re.findall(r'<a class="item" (.*?)</a>', resp.text, re.S)
        # res = []
        # for tag in tags[1:]:
        #     title = re.search(r'<div class="newtitle">(.*?)</div>', tag, re.S).group(1)
        #     price = re.search(r'<div class="price">(\d+)</div>', tag).group(1)
        #     o_price = re.search(r'<div class="o-price">(\d+)</div>', tag).group(1)
        #     sale = re.search(r'<span class="soldNumNew">已售(\d+)</span>', tag).group(1)
        #     print(title, price, o_price, sale)
        #     res.append(CouponModel(
        #         old_price=float(o_price),
        #         now_price=float(price),
        #         saled_count=int(sale),
        #         name=title))
        # return res
        cnt = 1
        while True and cnt < 3:
            try:
                self.params["power"] = 5
                res = self.session.get(UrlModel.coupon_url, params=self.params).json()
            except (Exception, JSONDecodeError):
                time.sleep(3)
                cnt += 1
            else:
                return [CouponModel(
                    old_price=conpon_msg["marketPrice"],
                    now_price=conpon_msg["price"],
                    saled_count=conpon_msg["sales"],
                    name=conpon_msg["productTitle"], )
                    for conpon_msg in res["dealDetails"]]
        return []

    def get_shop_story(self):
        """品牌故事 和推荐菜品及价格"""
        res = self.session.get(UrlModel.recommend_menu_price_url, params=self.params).json()
        story = res["poiShopBrand"]["story"]  # 品牌故事
        menu_price = [i["finalPrice"] for i in res["dishesWithPic"]]
        recommend_menu = dict(zip(self.comments_parser.recommend_menu, menu_price))  # 推荐菜品及价格
        # 评论信息
        return story, recommend_menu


class CommentsParser:
    def __init__(self, session, params):
        # 需要 shopid cityId shopType
        self.session = session
        self.params = params.copy()
        self.params.update(cityId=8, shopType=10)
        self.res = self._get_response()
        retry_time = 0
        while retry_time < 3 and not self.res:
            if not self.res:
                self.res = self._get_response()
            retry_time += 1

    @retry
    def _get_response(self):
        return self.session.get(UrlModel.recommend_url, params=self.params).json()

    @property
    def recommend_menu(self):
        return self.res["dishTagStrList"] if self.res["dishTagStrList"] else []

    def get_comments_info(self):
        all_count = self.res["reviewCountAll"]  # 所有评论
        bad_count = self.res["reviewCountBad"]  # 差评
        normal_count = self.res["reviewCountCommon"]  # 中评
        good_count = self.res["reviewCountGood"]  # 好评
        tags = [summary["summaryString"] for summary in self.res.get("summarys", [])] if self.res.get(
            "summarys") else []  # 标签
        return all_count, bad_count, normal_count, good_count, tags


class Crawler:
    def __init__(self, shop_id, headers=COMMON_HEADERS, session=requests.Session()):
        self.shop_id = shop_id
        self.headers = headers
        self.session = session
        self.session.headers = headers
        self.result = {"shop_id": shop_id}

    def crawl_page(self):
        response = self.session.get(url=UrlModel.shop_url.format(self.shop_id))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            print(f"{response.url} 抓取失败")
        return response.text

    def get_font_file(self):
        ...

    def save_font_name(self, font_name):
        with open("crawled_font", "a") as fp:
            fp.write(font_name + "\n")

    def parse_base_page(self, text):
        sel = Selector(text=text)
        self.result["per_capita"] = FontMapper.map(sel.xpath(BaseInfoSelectorXpathRules.per_capita_rule).getall())
        self.result["taste_score"] = FontMapper.map(sel.xpath(BaseInfoSelectorXpathRules.taste_score_rule).getall())
        self.result["env_score"] = FontMapper.map(sel.xpath(BaseInfoSelectorXpathRules.env_score_rule).getall())
        self.result["service_score"] = FontMapper.map(sel.xpath(BaseInfoSelectorXpathRules.service_score_rule).getall())
        self.result["address"] = FontMapper.map(sel.xpath(BaseInfoSelectorXpathRules.shop_address_rule).getall())
        self.result["phone"] = FontMapper.map(sel.xpath(BaseInfoSelectorXpathRules.shop_phone_rule).getall())
        self.result["other_shops"] = FontMapper.map(sel.xpath(BaseInfoSelectorXpathRules.other_shop_rule).getall())
        self.result["opening_time"] = FontMapper.map(sel.xpath(BaseInfoSelectorXpathRules.open_time_rule).getall())
        self.result["shop_name"] = FontMapper.map(sel.xpath(BaseInfoSelectorXpathRules.shop_name_rule).get().strip())

        css_name = re.search(r'//s3plus\.meituan\.net/v1/mss_(.*?)\.css', text).group(1)
        self.parse_css_file(css_name)

    def parse_css_file(self, css_name):
        text = requests.get(UrlModel.font_css_url.format(css_name)).text
        address = re.search(r"PingFangSC-Regular-address.*//(s3plus.*?woff).*\.address", text).group(1)
        self.save_font(address, "address")

        hours = re.search(r"PingFangSC-Regular-hours.*//(s3plus.*?woff).*\.hours", text).group(1)
        self.save_font(hours, "hours")

        shopdesc = re.search(r"PingFangSC-Regular-shopdesc.*//(s3plus.*?woff).*\.shopdesc", text).group(1)
        self.save_font(shopdesc, "shopdesc")

        dishname = re.search(r"PingFangSC-Regular-dishname.*//(s3plus.*?woff).*\.dishname", text).group(1)
        self.save_font(dishname, "dishname")

        num = re.search(r"PingFangSC-Regular-num.*//(s3plus.*?woff).*\.num", text).group(1)
        self.save_font(num, "num")

    def save_font(self, font_url: str, font_path):

        font_name = font_url.rsplit("/", maxsplit=1)[-1]
        print(font_url)
        if self.check_font_is_download(font_url):
            return
        Path(f"{font_path}/{font_name}").write_bytes(requests.get(UrlModel.pre_fix + font_url).content)
        self.save_font_url(font_url)

    def save_font_url(self, font_url):
        with open("crawled_font", "a") as fp:
            fp.write(font_url + "\n")

    def check_font_is_download(self, font_name):
        return font_name in set(Path("crawled_font").read_text().split())

    def run(self):
        self.parse_base_page(self.crawl_page())
        other_msg = AllMsgGenerator(self.shop_id, self.session)
        self.result["order_nums"] = other_msg.get_order_num()
        self.result["promotions"] = other_msg.get_coupon_data()
        self.result["comments_num"], self.result["bad_review_num"], self.result["mid_review_num"], \
        self.result["good_review_num"], self.result["comment_tags"] = other_msg.comments_data
        self.result["story"], self.result["recommend_menu"] = other_msg.get_shop_story()

        print(f"抓取结果{'-' * 50}")
        print(self.result)
        return self.result


@dataclass
class ShopModel:
    shop_name: str
    shop_score: float
    other_shops: list
    order_nums: int

    per_capita: float
    taste_score: float
    env_score: float
    service_score: float

    address: str
    phone: str
    special: list

    promotions: list
    recommend_menu: dict
    story: str

    user_tags: list
    comments_num: int
    comment_tags: list
    good_review_num: int
    mid_review_num: int
    bad_review_num: int

    opening_time: str


def get_all_shop_id():
    return set(Path("dp_02.csv").read_text().split("\n")[1:9001])


def record_shop_id(shop_id):
    file_name = "used_id.csv"
    with open(file_name, "a") as fp:
        fp.write(shop_id + "\n")


def get_crawled_shop_id():
    return set(Path("used_id.csv").read_text().split("\n"))


def save_data_to_file(data):
    with open("data.txt", "a", encoding="u8") as fp:
        fp.write(data + "\n")

def init():
    Path("crawled_font").touch(exist_ok=True)
    Path("address").mkdir(exist_ok=True)
    Path("num").mkdir(exist_ok=True)
    Path("hours").mkdir(exist_ok=True)
    Path("dishname").mkdir(exist_ok=True)
    Path("review").mkdir(exist_ok=True)
    Path("shopdesc").mkdir(exist_ok=True)


if __name__ == '__main__':
    # shop_id = "H1aHdhkb51pd6oXh"
    # Crawler(shop_id).run()
    init()
    while True:
        try:
            crawled_id = get_crawled_shop_id()
            for shop_id in get_all_shop_id():
                if shop_id not in crawled_id:
                    res = Crawler(shop_id).run()
                    save_data_to_file(json.dumps(res))
                    record_shop_id(shop_id)

                    print("数据存储成功")
                    time.sleep(15)
            else:
                break
        except Exception:
            print("抓取失败，即将重试。。。", traceback.print_exc())
            time.sleep(15)
