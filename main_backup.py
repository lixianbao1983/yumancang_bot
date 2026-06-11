import time

from signals.signal_engine import get_signal
from risk.risk_manager import RiskManager
from execution.paper_trader import PaperTrader


# =========================
# 初始化
# =========================

risk = RiskManager()
executor = PaperTrader()

portfolio = None
daily_count = 0


# =========================
# 模拟行情源（防止 market 缺失直接崩）
# =========================

def get_market_data():
    return {
        "prices": {
            "BTC/USDT": 120,
            "ETH/USDT": 60
        }
    }


# =========================
# 主循环
# =========================

while True:

    market_data = get_market_data()

    print(f"📡 行情: {market_data}")

    prices = market_data.get("prices", {})

    # 模拟 portfolio（如果你真实系统有就替换）
    class DummyPortfolio:
        equity = 1000
        cash = 1000
        def update_mark_to_market(self, prices): pass
        def get_quantity(self, symbol): return 0

    if portfolio is None:
        portfolio = DummyPortfolio()

    portfolio.update_mark_to_market(prices)

    # 信号
    signal = get_signal(market_data)

    symbol = signal.get("symbol", "BTC/USDT")
    action = signal.get("signal", "HOLD")

    # 风控
    allowed, reason = risk.check_risk(
        symbol=symbol,
        action=action,
        volume=0.001,
        tick=market_data,
        portfolio=portfolio,
        daily_trade_count=daily_count
    )

    print(f"🛡️ 风控: {allowed} | {reason}")

    if not allowed:
        time.sleep(2)
        continue

    # 执行
    if action != "HOLD":

        price = prices.get(symbol, 0)

        print(f"⚡ 下单: {action} {symbol} @ {price}")

        result = executor.execute_real_order(
            symbol=symbol,
            side=action,
            qty=0.001,
            price=price
        )

        print(f"🧾 成交: {result}")

    time.sleep(2)
