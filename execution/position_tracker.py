class PositionTracker:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.positions = {}
        self.avg_price = {}
        self.pnl = {}

    def get_quantity(self, symbol):
        return self.positions.get(symbol, 0)

    def get_pnl(self, symbol):
        return self.pnl.get(symbol, 0)

    def update(self, symbol, side, qty, price):

        current_qty = self.positions.get(symbol, 0)
        current_avg = self.avg_price.get(symbol, 0)

        # =========================
        # BUY
        # =========================
        if side == "BUY":
            new_qty = current_qty + qty

            if current_qty == 0:
                new_avg = price
            else:
                new_avg = (current_avg * current_qty + price * qty) / new_qty

            self.positions[symbol] = new_qty
            self.avg_price[symbol] = new_avg

        # =========================
        # SELL
        # =========================
        elif side == "SELL":
            new_qty = current_qty - qty

            if new_qty <= 0:
                self.positions[symbol] = 0
                self.avg_price[symbol] = 0
            else:
                self.positions[symbol] = new_qty

        # =========================
        # PnL 计算（安全版）
        # =========================
        qty_now = self.positions.get(symbol, 0)
        avg = self.avg_price.get(symbol, price)

        if qty_now > 0:
            self.pnl[symbol] = (price - avg) * qty_now
        else:
            self.pnl[symbol] = 0

        # =========================
        # 同步 portfolio（关键闭环）
        # =========================
        self.portfolio.update_fill(symbol, side, qty, price)
