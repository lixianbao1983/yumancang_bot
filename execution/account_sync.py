class AccountSync:
    def __init__(self, client):
        self.client = client

    def snapshot(self):
        raw = self.client.get_balances()

        # =========================
        # ✅ 兼容 Gate 返回格式（dict / list）
        # =========================
        if isinstance(raw, dict):
            # GateExecutor 当前返回结构：{ "USDT": {"available": x, "locked": y}, ... }
            raw = [
                {
                    "currency": k,
                    "available": v.get("available", 0),
                    "locked": v.get("locked", 0)
                }
                for k, v in raw.items()
                if isinstance(v, dict)
            ]

        elif isinstance(raw, str):
            import json
            raw = json.loads(raw)

        # =========================
        # 初始化账户数据
        # =========================
        cash = 0.0
        positions = {}
        total_value = 0.0

        # =========================
        # 遍历资产
        # =========================
        for item in raw:

            if not isinstance(item, dict):
                continue

            currency = item.get("currency")
            available = float(item.get("available", 0))
            locked = float(item.get("locked", 0))

            amount = available + locked

            # 💰 USDT 视为现金
            if currency == "USDT":
                cash = amount
                total_value += amount
            else:
                positions[currency] = amount
                total_value += amount

        # =========================
        # 🧠 equity 估值修正
        # =========================
        if total_value < 1:
            equity = 10000.0   # 初始虚拟锚定
        else:
            equity = total_value * 1  # 实盘模式：不再放大（避免假收益）

        return {
            "cash": cash,
            "positions": positions,
            "equity": equity
        }
