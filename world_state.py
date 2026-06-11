class WorldState:
    def __init__(self):
        # ======================
        # 📊 市场数据
        # ======================
        self.market = {}   # symbol -> tick

        # ======================
        # 💰 账户数据
        # ======================
        self.portfolio = {
            "cash": 10000,
            "equity": 10000
        }

        # ======================
        # 📉 风控状态
        # ======================
        self.risk = {
            "daily_trade_count": 0,
            "max_drawdown": -1000
        }

        # ======================
        # ⚙️ 执行状态
        # ======================
        self.execution = {
            "last_order": None
        }

    def update_tick(self, symbol, tick):
        self.market[symbol] = tick
