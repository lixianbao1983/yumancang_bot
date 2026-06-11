import os
import json
import logging

class PortfolioEngine:
    """
    全系统唯一的财务与仓位真理账本 (Single Source of Truth)
    采用工业级标准会计准则：Equity = Cash + 持仓市值。
    坚决杜绝已实现盈亏重复计价（Double Equity）的逻辑漏洞。
    """
    def __init__(self, initial_cash=10000.0):
        self.cash = float(initial_cash)
        self.positions = {}       
        self.avg_price = {}       
        self.realized_pnl = 0.0   
        self.unrealized_pnl = 0.0 
        self.equity = float(initial_cash)

    def get_quantity(self, symbol) -> float:
        return float(self.positions.get(symbol, 0.0))

    def get_pnl(self, symbol) -> float:
        if symbol in self.positions and symbol in self.avg_price:
            return self.unrealized_pnl
        return 0.0  

    def update_by_trade(self, symbol, side, qty, price, fee=0.0):
        qty = float(qty)
        price = float(price)
        fee = float(fee)

        if symbol not in self.positions:
            self.positions[symbol] = 0.0
            self.avg_price[symbol] = 0.0

        if side.upper() == "BUY":
            old_qty = self.positions[symbol]
            old_avg = self.avg_price[symbol]
            new_qty = old_qty + qty
            if new_qty > 0:
                self.avg_price[symbol] = (old_qty * old_avg + qty * price) / new_qty
            self.cash -= (qty * price + fee)
            self.positions[symbol] = new_qty

        elif side.upper() == "SELL":
            if self.positions[symbol] <= 0:
                return
            old_qty = self.positions[symbol]
            pnl = (price - self.avg_price[symbol]) * qty - fee
            self.realized_pnl += pnl
            self.cash += (qty * price - fee)
            self.positions[symbol] -= qty
            if self.positions[symbol] <= 0:
                self.positions[symbol] = 0.0
                self.avg_price[symbol] = 0.0
        logging.info(f"📋 账本单向变更成功 | {side} {symbol} 数量:{qty} | 剩余现金: {self.cash:.2f}")

    def update_mark_to_market(self, current_prices: dict):
        asset_value = 0.0
        self.unrealized_pnl = 0.0
        for symbol, qty in self.positions.items():
            if qty > 0:
                market_price = float(current_prices.get(symbol, 0.0))
                if market_price == 0.0:
                    market_price = self.avg_price.get(symbol, 0.0)
                asset_value += qty * market_price
                self.unrealized_pnl += (market_price - self.avg_price[symbol]) * qty
        self.equity = self.cash + asset_value

    def save(self, path="/home/ec2-user/trading_bot/state.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = {
            "cash": self.cash,
            "positions": self.positions,
            "avg_price": self.avg_price,
            "realized_pnl": self.realized_pnl,
            "unrealized_pnl": self.unrealized_pnl,
            "equity": self.equity,
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self, path="/home/ec2-user/trading_bot/state.json"):
        if not os.path.exists(path):
            return
        try:
            with open(path, "r") as f:
                data = json.load(f)
            self.cash = data.get("cash", self.cash)
            self.positions = data.get("positions", {})
            self.avg_price = data.get("avg_price", {})
            self.realized_pnl = data.get("realized_pnl", 0.0)
            self.unrealized_pnl = data.get("unrealized_pnl", 0.0)
            self.equity = data.get("equity", self.cash)
        except Exception as e:
            logging.error(f"读取状态文件失败: {e}")

    def snapshot(self):
        return {
            "cash": self.cash,
            "equity": self.equity,
            "realized_pnl": self.realized_pnl,
            "unrealized_pnl": self.unrealized_pnl,
            "positions": self.positions,
        }
