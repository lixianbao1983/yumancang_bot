class PaperTrader:
    def __init__(self, portfolio=None, risk_gate=None):
        self.portfolio = portfolio
        self.risk_gate = risk_gate

    def execute_trade(self, symbol, side, qty, price, fee=0.0):
        trade = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price,
            "fee": fee,
            "status": "FILLED"
        }

        print(f"[TRADE EXECUTED] {side} {symbol} {qty} @ {price}")

        self._log_trade(trade)

        return trade

    def _log_trade(self, trade: dict):
        print(f"[LOG] {trade}")
