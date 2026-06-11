import time


class RiskManager:
    """
    统一风控模块（实盘标准版）
    """

    def __init__(self):
        self.max_position = 0.01
        self.max_trades_per_minute = 30
        self.halt = False
        self.trade_counter = 0
        self.last_reset = time.time()

        print("[RISK INIT] RiskManager 已启动 ✅")

    def check_halt(self):
        now = time.time()

        if now - self.last_reset > 60:
            self.trade_counter = 0
            self.last_reset = now

        return self.halt or self.trade_counter >= self.max_trades_per_minute

    def record_trade(self):
        self.trade_counter += 1

    def allow(self, symbol, side, qty, price, portfolio=None):

        if self.check_halt():
            return False, "RISK_HALT"

        if qty > self.max_position:
            return False, "POSITION_LIMIT"

        if side not in ["BUY", "SELL"]:
            return False, "INVALID_SIDE"

        if portfolio and portfolio.get("equity", 0) <= 0:
            return False, "EQUITY_INVALID"

        return True, "OK"
