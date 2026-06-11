class RiskManager:

    def __init__(self, max_position_size=100.0):
        self.max_position_size = max_position_size

    def check_risk(self, symbol, action, volume, tick, portfolio, daily_trade_count):

        if portfolio is None:
            return False, "NO_PORTFOLIO"

        if portfolio["equity"] <= 0:
            return False, "EQUITY_BROKEN"

        if portfolio["cash"] < 0:
            return False, "CASH_NEGATIVE"

        if daily_trade_count > 10:
            return False, "DAILY_LIMIT"

        current_pos = portfolio["positions"].get(symbol, 0)

        if action.upper() == "BUY":
            if current_pos + volume > self.max_position_size:
                return False, "POSITION_LIMIT"

        price_data = tick.get("prices", {})
        price = float(price_data.get(symbol, 0.0))

        max_exposure = portfolio["equity"] * 0.5
        exposure = current_pos * price

        if exposure > max_exposure:
            return False, "EXPOSURE_LIMIT"

        return True, "OK"
