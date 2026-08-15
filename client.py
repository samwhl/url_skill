"""
Skill Demo 客户端调用示例

别人在代码中可以直接复用这个 Client 类，
或者参考下面的 if __name__ == "__main__" 用法。
"""
import requests


class SkillDemoClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 5000):
        self.base_url = f"http://{host}:{port}"

    def index(self) -> dict:
        """获取欢迎信息和接口列表"""
        resp = requests.get(f"{self.base_url}/")
        resp.raise_for_status()
        return resp.json()

    def hello(self, name: str = "World") -> dict:
        """传名字，返回问候"""
        resp = requests.get(f"{self.base_url}/hello", params={"name": name})
        resp.raise_for_status()
        return resp.json()

    def echo(self, data: dict) -> dict:
        """POST 发送 JSON，服务端原样返回"""
        resp = requests.post(f"{self.base_url}/echo", json=data)
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    # 使用示例：别人只要改 host/port 就能连你的服务
    client = SkillDemoClient(host="127.0.0.1", port=5000)

    print("1) GET /")
    print(client.index())

    print("\n2) GET /hello?name=Trae")
    print(client.hello("Trae"))

    print("\n3) POST /echo")
    print(client.echo({"msg": "hi", "num": 42}))
