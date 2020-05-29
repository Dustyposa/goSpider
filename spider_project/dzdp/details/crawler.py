import time
from dataclasses import dataclass
from datetime import datetime

import requests
from parsel import Selector, css2xpath
from headers import COMMON_HEADERS
from resource.font.map import address_mapping, review_tag_mapping, shop_num_mapping


class FontMapper:
    def __init__(self):
        ...


class PageParser:
    def __init__(self, text: str):
        self.sel = Selector(text)


@dataclass
class SelectorXpathRules:
    comments_num_rule = css2xpath("#reviewCount .num::text")
    per_capita_rule = css2xpath("#avgPriceTitle .num::text")
    taste_score_rule = css2xpath("#comment_score") + "/span[contains(text(), '口味')]/d/text()"


class Crawler:
    def __init__(self, url: str):
        self.url = url
        self.headers = COMMON_HEADERS

    def crawl_page(self):
        reseponse = requests.get(self.url, headers=self.headers)
        try:
            reseponse.raise_for_status()
        except requests.HTTPError:
            print(f"{self.url} 抓取失败")

        return reseponse.text

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
