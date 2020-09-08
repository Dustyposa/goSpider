from dataclasses import dataclass
from typing import List

import requests
from parsel import Selector
from PIL import Image, ImageDraw, ImageFont

from small_projects.文字生成图片.config import HOT_LIST_URL

font = ImageFont.truetype("AaTianShiZhuYi-2.ttf")


# img = Image.new('RGB', (200, 100), (255, 255, 255))
# d = ImageDraw.Draw(img)
# d.text((20, 20), 'Hello', fill=(255, 0, 0))
#
# with open("res.png", "wb") as fp:
#     img.save(fp, 'png')
# print("生成图片成功")

@dataclass
class SingleData:
    title: str
    heat: str


@dataclass
class HotData:
    name: str
    data: List[SingleData]
    scope: str


class HotListCrawler:
    url = HOT_LIST_URL
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }

    @classmethod
    def crawl(cls) -> List[HotData]:
        web_data = cls._get_web_data()
        return cls._parse_web_data(web_data)

    @classmethod
    def _get_web_data(cls) -> str:
        return requests.get(cls.url, headers=cls.headers).content.decode("u8")

    @classmethod
    def _parse_web_data(cls, web_data: str) -> List[HotData]:
        res = []
        sel = Selector(text=web_data)
        for hot_data in sel.css(".cc-cd")[:4]:
            name = hot_data.css(".cc-cd-lb>span::text").get()
            scope = hot_data.css(".cc-cd-sb-st::text").get()
            data = []
            for single_data in sel.css(".cc-cd-cb-ll")[:10]:
                title = single_data.css(".t::text").get()
                heat = single_data.css(".e::text").get()
                data.append(SingleData(title=title, heat=heat))
            res.append(HotData(
                name=name,
                scope=scope,
                data=data
            ))
        return res


class PngProducer:
    @classmethod
    def draw_from_hot_data(cls, data: List[HotData]):
        data_length = len(data)
        img = Image.new('RGB', (400, 300 * data_length), (255, 255, 255))
        drawer = ImageDraw.Draw(img)
        base_x, base_y = 10, 10
        for hot_data in data:
            drawer.text((base_x, base_y), hot_data.name, fill=(255, 0, 0),
                        font=font)
            base_y += 20
            for single_data in hot_data.data:
                drawer.text((base_x, base_y), single_data.title, fill=(255, 0, 0),
                            font=font)
                drawer.text((base_x + 200, base_y), single_data.heat, fill=(255, 0, 0),
                            font=font)
                base_y += 15

        cls.save(img)

    @classmethod
    def save(cls, img):
        with open("res.png", "wb") as fp:
            img.save(fp, 'png')
            print("生成图片成功")


if __name__ == '__main__':
    data = HotListCrawler.crawl()
    PngProducer.draw_from_hot_data(data)
