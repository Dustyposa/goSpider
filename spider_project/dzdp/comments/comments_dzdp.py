import time
from typing import Dict, Any

import requests
import pymongo
from parsel import Selector
from pathlib import Path

from headers import COMMENTS_HEADERS


class DBClient:
    def __init__(self, db_name: str) -> None:
        self.client = pymongo.MongoClient('mongodb://mongo:27017/')
        self.db = self.client[db_name]
        self.col = self.db["comments"]

    def insert_one(self, data: Dict[str, Any]) -> str:
        return self.col.insert_one(data)


class CommentsParser:
    def __init__(self, html: str) -> None:
        self.selector = Selector(text=html)
        self.check_recommend = 0

    @property
    def is_not_empty_page(self) -> bool:
        return len(self.selector.css(".reviews-wrapper")) != 0

    @property
    def has_recommend(self) -> bool:
        return len(self.selector.css(".review-recommend")) != 0


class CommentsCrawler:
    def __init__(self, shop_id: str) -> None:
        self.shop_id = shop_id
        self.base_url = f"http://www.dianping.com/shop/{self.shop_id}/review_all/p"
        self.now_page = 8
        self.crawl_url = self.base_url + str(self.now_page)
        self.headers = COMMENTS_HEADERS
        self.db_client = DBClient("dzdp")
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.now_content = b""

    def increase_page(self) -> None:
        self.now_page += 1
        self.crawl_url = self.base_url + str(self.now_page)

    def run(self) -> None:
        while True:
            print(f"正在抓取:{self.crawl_url}")
            parser = self.crawl_page()
            if parser.is_not_empty_page and parser.has_recommend:
                self.db_client.insert_one({
                    "text": parser.selector.xpath("//body").get(),
                    "page_nums": self.now_page,
                    "shop_id": self.shop_id,
                    "url": self.crawl_url,
                })
                self.increase_page()
            else:
                print("没有数据了。")
                self.record_id()
                break
            time.sleep(15)

    def record_id(self) -> None:
        Path("fail_data").write_bytes(self.now_content)
        with open("crawled_db", "a") as fp:
            fp.write(f"{self.shop_id},{self.now_page}\n")

    def crawl_page(self) -> CommentsParser:
        if self.now_page > 1:
            self.session.headers["Referer"] = self.base_url + str(self.now_page - 1)
        # print(self.session.headers)
        response = self.session.get(self.crawl_url)
        response.raise_for_status()
        self.now_content = response.content
        text = response.text
        parser = CommentsParser(html=text)
        return parser


if __name__ == '__main__':
    CommentsCrawler("67408602").run()
