import re
import time
from dataclasses import dataclass
from datetime import datetime

import requests
from parsel import Selector, css2xpath
from headers import COMMON_HEADERS
# from resource.font.map import address_mapping, review_tag_mapping, shop_num_mapping


class UrlModel:
    coupon_url = "http://www.dianping.com/ajax/json/shopDynamic/promoInfo"  # 优惠促销
    ordered_url = "https://reserve.dianping.com/plusdom/poidetail"  # 预定人数
    recommend_url = "http://www.dianping.com/ajax/json/shopDynamic/allReview"  # 推荐菜
    recommend_menu_price_url = "http://www.dianping.com/ajax/json/shopDynamic/shopTabs"  # 推荐菜价格
    shop_url = "http://www.dianping.com/shop/{}"
    m_shop_url = 'https://m.dianping.com/shop/{}'


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
                           'cityId': 8}
        self.params["shopId"] = shop_id
        self.comments_parser = CommentsParser(self.session, self.params)  # 推荐菜
        self.comments_data = self.comments_parser.get_comments_info()

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
        resp = requests.get(url=url, headers=COMMON_HEADERS)
        tags = re.findall(r'<a class="item" (.*?)</a>', resp.text, re.S)
        res = []
        for tag in tags[1:]:
            title = re.search(r'<div class="newtitle">(.*?)</div>', tag, re.S).group(1)
            price = re.search(r'<div class="price">(\d+)</div>', tag).group(1)
            o_price = re.search(r'<div class="o-price">(\d+)</div>', tag).group(1)
            sale = re.search(r'<span class="soldNumNew">已售(\d+)</span>', tag).group(1)
            print(title, price, o_price, sale)
            res.append(CouponModel(
                old_price=float(o_price),
                now_price=float(price),
                saled_count=int(sale),
                name=title))
        return res
        # res = self.session.get(UrlModel.coupon_url, params=self.params).json()
        # return [CouponModel(
        #     old_price=conpon_msg["marketPrice"],
        #     now_price=conpon_msg["price"],
        #     saled_count=conpon_msg["sales"],
        #     name=conpon_msg["productTitle"], )
        #     for conpon_msg in res["dealDetails"]]

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

    def _get_response(self):
        return self.session.get(UrlModel.recommend_url, params=self.params).json()

    @property
    def recommend_menu(self):
        return self.res["dishTagStrList"]

    def get_comments_info(self):
        all_count = self.res["reviewCountAll"]  # 所有评论
        bad_count = self.res["reviewCountBad"]  # 差评
        normal_count = self.res["reviewCountCommon"]  # 中评
        good_count = self.res["reviewCountGood"]  # 好评
        tags = [summary["summaryString"] for summary in self.res["summarys"]]  # 标签
        return all_count, bad_count, normal_count, good_count, tags


class Crawler:
    def __init__(self, shop_id, headers=COMMON_HEADERS, session=requests.Session()):
        self.shop_id = shop_id
        self.headers = headers
        self.session = session
        self.session.headers = headers
        self.result = {}

    def crawl_page(self):
        response = self.session.get(url=UrlModel.shop_url.format(self.shop_id))
        try:
            response.raise_for_status()
        except requests.HTTPError:
            print(f"{response.url} 抓取失败")
        return response.text

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


if __name__ == '__main__':
    shop_id = "H1aHdhkb51pd6oXh"
    Crawler(shop_id).run()
