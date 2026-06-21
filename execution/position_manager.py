import time

class PositionManager:

    def __init__(self):

        self.positions = {}
        self.trade_history = []

        # 默认止盈止损
        self.tp = 0.02   # +2%
        self.sl = -0.01  # -1%

    # =========================
    # 开仓记录
    # =========================
    def open_position(self, signal, entry_price):

        symbol = signal["symbol"]

        self.positions[symbol] = {
            "symbol": symbol,
            "side": signal["action"],
            "qty": signal["qty"],
            "entry_price": entry_price,
            "time": time.time(),
            "pnl": 0.0
        }

        print(f"📥 OPEN {symbol} @ {entry_price}")

    # =========================
    # 获取持仓
    # =========================
    def get_positions(self):
        return self.positions

    # =========================
    # 更新 & 检查退出
    # =========================
    def check_exit(self, symbol, price):

        if symbol not in self.positions:
            return None

        pos = self.positions[symbol]

        entry = pos["entry_price"]
        side = pos["side"]

        if side == "BUY":
            pnl = (price - entry) / entry
        else:
            pnl = (entry - price) / entry

        pos["pnl"] = pnl

        # 止盈
        if pnl >= self.tp:
            return self._close(symbol, price, "TP")

        # 止损
        if pnl <= self.sl:
            return self._close(symbol, price, "SL")

        return None

    # =========================
    # 平仓
    # =========================
    def _close(self, symbol, price, reason):

        pos = self.positions[symbol]

        record = {
            "symbol": symbol,
            "entry": pos["entry_price"],
            "exit": price,
            "pnl": pos["pnl"],
            "reason": reason
        }

        self.trade_history.append(record)

        print(f"📤 CLOSE {symbol} | {reason} | pnl={pos['pnl']:.4f}")

        del self.positions[symbol]

        return record
