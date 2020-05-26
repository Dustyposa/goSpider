import time
from dataclasses import dataclass
from datetime import datetime

import requests

from headers import COMMON_HEADERS
from resource.font import address_mapping, review_tag_mapping, shop_num_mapping


class FontMapper:
    def __init__(self):
        ...


class PageParser:
    def __init__(self):
        ...


class Crawler:
    def __init__(self):
        ...


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




