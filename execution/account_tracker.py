from portfolio.portfolio_engine import PortfolioEngine


class AccountTracker:
    def __init__(self, initial_cash: float = 10000):
        self.portfolio = PortfolioEngine(initial_cash=initial_cash)

    def get_quantity(self, symbol: str) -> float:
        return self.portfolio.positions.get(symbol, 0.0)

    def get_pnl(self, symbol: str = None) -> float:
        return self.portfolio.realized_pnl + self.portfolio.unrealized_pnl

    def get_equity(self) -> float:
        return self.portfolio.equity

    def update_fill(self, symbol, side, qty, price, fee=0.0):
        self.portfolio.update_fill(symbol, side, qty, price, fee)

    def snapshot(self):
        return self.portfolio.snapshot()
