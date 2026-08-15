"""
简单的模型调用示例

读取 .env 中的配置，调用 SiliconFlow（OpenAI 兼容）接口，
发送一句问候并打印模型回复。
"""
import os
import requests


def load_env(env_path: str = ".env") -> dict:
    """简单解析 .env 文件，返回配置字典"""
    config = {}
    if not os.path.exists(env_path):
        return config
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            config[key.strip()] = value.strip()
    return config


def chat(prompt: str, config: dict) -> str:
    """调用聊天接口，返回模型回复文本"""
    url = config["model_url"].rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {config['model_api_key']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config["model_name"],
        "messages": [
            {"role": "system", "content": "你是一个简洁的助手。"},
            {"role": "user", "content": prompt},
        ],
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    cfg = load_env()
    if not cfg:
        print("未找到 .env 配置文件")
        raise SystemExit(1)

    question = "用一句话介绍一下你自己。"
    print(f"提问：{question}")

    answer = chat(question, cfg)
    print(f"回复：{answer}")
