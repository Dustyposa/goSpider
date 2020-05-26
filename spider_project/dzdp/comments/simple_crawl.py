import time

import requests
from parsel import Selector

from headers import COMMENTS_HEADERS

base_url = "http://www.dianping.com/shop/67408602/review_all/p{}"


for i in range(1, 10):
    if i > 1:
        COMMENTS_HEADERS["Referer"] = base_url.format(i - 1)
    res = requests.get(base_url.format(1), headers=COMMENTS_HEADERS)
    selector = Selector(text=res.text)
    if selector.css(".review-recommend").getall():
        print(selector.css(".review-recommend").getall())
    else:
        print(base_url.format(1))
        print(res.content.decode("u8"))
    time.sleep(5)

