from time import sleep

from flask import Flask, jsonify, Response

app: Flask = Flask(__name__)

retry_count: int = 0  # 用于重试请求的计数


@app.route("/api/retry", methods=["GET"])
def retry_api() -> Response:
    """
    延时 1s 的请求接口， 响应时间 > 1s。
    :return:
    """
    global retry_count
    retry_count += 1
    print(f"这是第{retry_count}次请求")
    if retry_count < 3:
        sleep(1)
    else:
        retry_count = 0  # 计数清零
    return jsonify({"msg": "已经三次了哦！"})


if __name__ == '__main__':
    app.run()
