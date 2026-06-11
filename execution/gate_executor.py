import os
from dotenv import load_dotenv

load_dotenv()

from execution.gate_client import GateClient


class GateExecutor:
    def __init__(self):
        self.client = GateClient(
            api_key=os.getenv("GATE_API_KEY"),
            api_secret=os.getenv("GATE_API_SECRET")
        )

    # ======================
    # 行情
    # ======================
    def get_market_data(self):
        tickers = self.client.get_ticker("BTC_USDT")

        prices = {}

        if isinstance(tickers, list):
            for t in tickers:
                prices[t["currency_pair"]] = float(t["last"])

        return {"prices": prices}

    # ======================
    # 账户
    # ======================
    def get_account(self):
        raw = self.client.get_balances()

        if not isinstance(raw, list):
            print("[GATE ERROR]", raw)
            return {}

        balances = {}

        for item in raw:
            if not isinstance(item, dict):
                continue

            balances[item["currency"]] = {
                "available": float(item.get("available", 0)),
                "locked": float(item.get("locked", 0))
            }

        return balances

    # ======================
    # 下单
    # ======================
    def execute_trade(self, symbol, side, qty, price=None):
        result = self.client.place_order(
            symbol=symbol,
            side=side,
            amount=qty,
            price=price
        )

        return {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "status": "LIVE",
            "gate_response": result
        }
