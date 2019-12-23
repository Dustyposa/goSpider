from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/api', methods=["GET"])
def msg_api():
    """常规返回"""
    return jsonify({'Hello': 'World!'})


@app.route('/goods/<int:goods_id>', methods=["GET"])
def query_goods(goods_id):
    """带id的路由"""
    return jsonify({"name": "cake", "id": goods_id})


@app.route('/po', methods=["POST"])
def po():
    # json_data = request.form
    filename = request.form.get('name')
    request.files.get('data').save(filename)
    return jsonify({'stats': 'ok'})


@app.errorhandler(404)
def error_404_handing(error):
    """404页面"""
    return jsonify({"msg": "no route", "err": str(error)}), 404


if __name__ == '__main__':
    app.run(port=80)
