from time import sleep

from flask import Flask, jsonify, Response

app: Flask = Flask(__name__)
retry_count: int = 0


@app.route("/api/retry", methods=["GET"])
def retry_api() -> Response:
    global retry_count
    retry_count += 1
    print(f"这是第{retry_count}次请求")
    if retry_count < 3:
        sleep(1)
    return jsonify({"msg": "已经三次了哦！"})


if __name__ == '__main__':
    app.run()
