class PositionManager:

    def __init__(self):
        self.positions = {}

        # 🧠 风控参数
        self.tp = 0.015   # +1.5% 止盈
        self.sl = -0.008  # -0.8% 止损

    def get_positions(self):
        return self.positions

    def has_position(self, symbol):
        return symbol in self.positions

    def open_position(self, signal, price):

        symbol = signal["symbol"]

        if symbol in self.positions:
            return

        self.positions[symbol] = {
            "symbol": symbol,
            "qty": signal["qty"],
            "entry_price": price
        }

        print(f"📥 OPEN: {symbol} @ {price}")

    def update_price(self, symbol, price):

        if symbol not in self.positions:
            return

        pos = self.positions[symbol]
        entry = pos["entry_price"]

        change = (price - entry) / entry

        # 🧠 盈亏计算
        pos["pnl"] = change

        print(f"📊 {symbol} PnL: {change:.4f}")

        # 🔥 止盈
        if change > self.tp:
            self.close_position(symbol, price, "TP")

        # 🔻 止损
        elif change < self.sl:
            self.close_position(symbol, price, "SL")

    def close_position(self, symbol, price, reason):

        if symbol in self.positions:
            self.positions.pop(symbol)
            print(f"📤 CLOSE: {symbol} @ {price} ({reason})")
