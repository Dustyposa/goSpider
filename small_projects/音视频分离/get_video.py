from path import Path

import requests


def get_sources_to_max_num(url: str, max_num: int) -> None:
    for i in range(1, max_num + 1):
        if i < 10:
            tmp_url = url.format(f"0{i}")
        else:
            tmp_url = url.format(f"{i}")
        save_data(get_data(tmp_url), i)
        print(F"第{i}个存储完毕")


def get_data(url: str) -> bytes:
    return requests.get(url).content


def save_data(data: bytes, index: int):
    Path(f"./videos_files/{index}.mp4").write_bytes(data)


if __name__ == '__main__':
    url = "http://www.ynfn.gov.cn:7000/fnnews/py{}.mp4"
    get_sources_to_max_num(url, 81)
