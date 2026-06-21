import os


class GateAccount:
    """
    统一账户配置入口（只读环境变量）
    """

    def __init__(self):
        self.api_key = os.getenv("GATE_API_KEY")
        self.api_secret = os.getenv("GATE_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise ValueError(
                "❌ Missing GATE_API_KEY / GATE_API_SECRET in environment"
            )

    def get_headers(self):
        return {
            "KEY": self.api_key
        }
