from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """根路径，返回欢迎信息"""
    return jsonify({
        "message": "Hello from Skill Demo!",
        "endpoints": ["/", "/hello", "/echo"]
    })


@app.route("/hello", methods=["GET"])
def hello():
    """GET 示例：通过 query 参数传名字"""
    name = request.args.get("name", "World")
    return jsonify({"message": f"Hello, {name}!"})


@app.route("/echo", methods=["POST"])
def echo():
    """POST 示例：原样返回客户端发送的 JSON"""
    data = request.get_json(silent=True) or {}
    return jsonify({"received": data})


if __name__ == "__main__":
    # 监听 0.0.0.0 表示允许外部通过 IP 访问，端口 5000
    app.run(host="0.0.0.0", port=5000)
