"""
简单的 Excel Agent

具备打开 Excel 文件并读取数据的能力。
可结合 .env 中的模型配置，对 Excel 数据进行问答。

依赖：openpyxl  （pip install openpyxl）
"""
import os
import sys
import requests
import openpyxl


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
            {"role": "system", "content": "你是一个数据分析助手，根据提供的 Excel 数据回答问题。"},
            {"role": "user", "content": prompt},
        ],
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


class ExcelAgent:
    """简单的 Excel Agent：具备打开并读取 Excel 数据的工具能力"""

    def __init__(self, excel_path: str, config: dict = None):
        self.path = excel_path
        self.config = config or {}
        self._wb = None

    # ---- 工具能力 ----
    def open(self):
        """打开 Excel 工作簿"""
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Excel 文件不存在: {self.path}")
        self._wb = openpyxl.load_workbook(self.path, data_only=True)
        return self._wb

    def list_sheets(self) -> list:
        """列出所有工作表名称"""
        if self._wb is None:
            self.open()
        return self._wb.sheetnames

    def read_sheet(self, sheet_name: str = None, max_rows: int = 50) -> list:
        """读取指定工作表数据，返回二维列表（含表头）。默认读第一个 sheet"""
        if self._wb is None:
            self.open()
        ws = self._wb[sheet_name] if sheet_name else self._wb.active
        rows = []
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i >= max_rows:
                break
            rows.append([("" if c is None else str(c)) for c in row])
        return rows

    # ---- agent 主体 ----
    def run(self, question: str) -> str:
        """读取 Excel 数据，交给模型回答问题"""
        sheets = self.list_sheets()
        data_text = []
        for name in sheets:
            rows = self.read_sheet(name, max_rows=20)
            data_text.append(f"[Sheet: {name}]")
            for r in rows:
                data_text.append(" | ".join(r))
        data_str = "\n".join(data_text)

        if not self.config:
            return f"（未配置模型，以下为读取到的数据）\n{data_str}"

        prompt = (
            f"以下是 Excel 文件 {self.path} 的数据：\n\n"
            f"{data_str}\n\n请根据数据回答：{question}"
        )
        return chat(prompt, self.config)


if __name__ == "__main__":
    # 用法：python test.py <excel文件路径>
    if len(sys.argv) < 2:
        print("用法：python test.py <excel文件路径>")
        raise SystemExit(1)

    excel_path = sys.argv[1]
    cfg = load_env()

    agent = ExcelAgent(excel_path, cfg)
    print(f"工作表：{agent.list_sheets()}")

    question = "这份表格主要讲了什么？"
    print(f"\n问题：{question}")
    print(f"回答：{agent.run(question)}")
