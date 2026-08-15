"""
外部代码调用 Skill Demo 服务的示例

使用本文件无需依赖项目内的 client.py，
把本文件复制到任意项目里，确保服务端在跑即可调用。

依赖：pip install requests
"""
import requests

# 服务端地址：改成实际部署服务的主机 IP 和端口
# 本机调试用 127.0.0.1；同网段其他机器用服务端局域网 IP，例如 172.19.0.1
BASE_URL = "http://127.0.0.1:5000"


def call_index() -> dict:
    """GET / ：获取欢迎信息和接口列表"""
    resp = requests.get(f"{BASE_URL}/")
    print(resp)
    resp.raise_for_status()
    return resp.json()


def call_hello(name: str) -> dict:
    """GET /hello?name=xxx ：带 query 参数调用"""
    resp = requests.get(f"{BASE_URL}/hello", params={"name": name})
    resp.raise_for_status()
    return resp.json()


def call_echo(payload: dict) -> dict:
    """POST /echo ：发送 JSON，服务端原样返回"""
    resp = requests.post(f"{BASE_URL}/echo", json=payload)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    print("1) GET /")
    print(call_index())

    print("\n2) GET /hello?name=Trae")
    print(call_hello("Trae"))

    print("\n3) POST /echo")
    print(call_echo({"msg": "hi", "num": 42}))
