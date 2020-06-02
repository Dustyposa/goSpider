import re
import time
from dataclasses import dataclass
from datetime import datetime

import requests
from parsel import Selector, css2xpath
from headers import COMMON_HEADERS
from resource.font.map import address_mapping, review_tag_mapping, shop_num_mapping


class UrlModel:
    coupon_url = "http://www.dianping.com/ajax/json/shopDynamic/promoInfo"  # 优惠促销
    ordered_url = "https://reserve.dianping.com/plusdom/poidetail?shopId=H1aHdhkb51pd6oXh"  # 预定人数
    recommend_url = "http://www.dianping.com/ajax/json/shopDynamic/allReview"  # 推荐菜
    recommend_menu_price_url = "http://www.dianping.com/ajax/json/shopDynamic/shopTabs"  # 推荐菜价格


class FontMapper:
    def __init__(self):
        ...


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
    other_shop_rule = css2xpath(".more-shop")  # 更多店铺
    shop_phone_rule = css2xpath(".expand-info.tel ::text")  # 店铺电话


class AllMsgGenerator:
    def __init__(self, view_data):
        self.view_data = view_data
        self.res = {}
        self.comments_parser = CommentsParser("123")  # 推荐菜

    def get_order_num(self):
        """预定人数"""
        url = "https://reserve.dianping.com/plusdom/poidetail?shopId=H1aHdhkb51pd6oXh"
        content = requests.get(url).content.decode("u8")
        res = re.search(r"(\d+)人已订", content)
        if res:
            return res.group(1)
        return 0

    def get_coupon_data(self):
        """优惠券"""
        res = requests.get(UrlModel.coupon_url).json()
        return [CouponModel(
            old_price=conpon_msg["marketPrice"],
            now_price=conpon_msg["price"],
            saled_count=conpon_msg["sales"],
            name=conpon_msg["productTitle"],
        )
            for conpon_msg in res["dealDetails"]]

    def get_shop_story(self):
        """品牌故事 和推荐菜品及价格"""
        res = requests.get(UrlModel.recommend_menu_price_url).json()
        story = res["poiShopBrand"]["story"]  # 品牌故事
        menu_price = [i["finalPrice"] for i in res["dishesWithPic"]]
        recommend_menu = dict(zip(self.comments_parser.recommend_menu, menu_price))  # 推荐菜品及价格
        # 评论信息
        return


class CommentsParser:
    def __init__(self, url):
        self.url = url
        self.res = self._get_response()

    def _get_response(self):
        return requests.get(self.url).json()

    @property
    def recommend_menu(self):
        return self.res["dishTagStrList"]

    def get_comments_info(self):
        all_count = self.res["reviewCountAll"]  # 所有评论
        bad_count = self.res["reviewCountBad"]  # 差评
        normal_count = self.res["reviewCountCommon"]  # 中评
        good_count = self.res["reviewCountGood"]  # 好评
        tags = [summary["summaryString"] for summary in self.res["summarys"]]  # 标签
        return {"all": all_count}


class Crawler:
    def __init__(self, url: str):
        self.url = url
        self.headers = COMMON_HEADERS

    def crawl_page(self):
        response = requests.get(self.url, headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            print(f"{self.url} 抓取失败")

        return response.text

    def parse_page(self, text):
        sel = Selector(text=text)
        pass

    def run(self):
        self.parse_page(self.crawl_page())


@dataclass
class ShopModel:
    shop_name: str
    shop_score: float
    comments_num: int
    other_shops: list

    per_capita: float
    taste_score: float
    env_score: float
    service_score: float

    address: str
    phone: str
    special: list

    promotions: list
    recommend_menu: list

    user_tags: list
    good_review_num: int
    mid_review_num: int
    bad_review_num: int

    opening_time: datetime


if __name__ == '__main__':
    url = "http://www.dianping.com/shop/H1aHdhkb51pd6oXh"
    Crawler(url).run()
