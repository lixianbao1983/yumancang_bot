class Memory:

    def __init__(self):
        self.data = {
            "last_signal": None,
            "last_trade_time": 0,
            "cooldown": 5,
            "trade_count": 0
        }

    def can_trade(self):
        import time
        return time.time() - self.data["last_trade_time"] > self.data["cooldown"]

    def update_trade(self):
        import time
        self.data["last_trade_time"] = time.time()
        self.data["trade_count"] += 1
