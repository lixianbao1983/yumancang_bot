import time

class SignalEngine:

    def __init__(self):
        # 🧠 每个 symbol 单独记忆价格
        self.last_price = {}

        self.last_signal_time = {}
        self.cooldown = 5

    def generate(self, symbol, price):

        if price is None:
            return None

        now = time.time()

        # 🧠 冷却（按 symbol）
        if symbol in self.last_signal_time:
            if now - self.last_signal_time[symbol] < self.cooldown:
                return None

        last = self.last_price.get(symbol)

        # 🧠 初始化
        if last is None:
            self.last_price[symbol] = price
            return None

        change = (price - last) / last

        self.last_price[symbol] = price
        self.last_signal_time[symbol] = now

        # 🔥 BUY
        if change > 0.0002:
            return {
                "symbol": symbol,
                "action": "BUY",
                "qty": 1
            }

        # 🔻 SELL
        if change < -0.0002:
            return {
                "symbol": symbol,
                "action": "SELL",
                "qty": 1
            }

        return None
