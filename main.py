import time

from execution.gate_executor import GateExecutor
from execution.account_sync import AccountSync
from risk.risk_gate import RiskManager
from signals.strategy_signal import StrategySignal


# =====================
# 初始化
# =====================
executor = GateExecutor()
account_sync = AccountSync(executor.client)
risk = RiskManager()

strategies = [StrategySignal()]
daily_trade_count = 0


# =====================
# 主循环
# =====================
while True:

    # =====================
    # 行情
    # =====================
    market_data = executor.get_market_data()
    print(f"📡 行情: {market_data}")

    # =====================
    # 账户
    # =====================
    portfolio = account_sync.snapshot()
    print(f"💰 账户: {portfolio}")

    # =====================
    # 策略信号
    # =====================
    signals = []

    for s in strategies:
        try:
            sig = s.on_tick(market_data)
            if sig:
                signals.append(sig)
        except Exception as e:
            print(f"[STRATEGY ERROR] {e}")

    signal = signals[0] if signals else {
        "symbol": "BTC_USDT",
        "action": "HOLD",
        "qty": 0.001,
        "price": market_data["prices"]["BTC_USDT"]
    }

    print(f"📊 信号: {signal}")

    # =====================
    # 风控
    # =====================
    allowed, reason = risk.allow(
        signal["symbol"],
        signal["action"],
        signal["qty"],
        signal["price"],
        portfolio
    )

    print(f"🛡️ 风控: {allowed} | {reason}")

    # =====================
    # 执行（已统一 real_order）
    # =====================
    if allowed and signal["action"] != "HOLD":

        try:
            result = executor.execute_real_order(
                signal["symbol"],
                signal["action"],
                signal["qty"],
                signal["price"]
            )

            risk.record_trade()
            daily_trade_count += 1

            print(f"🧾 成交: {result}")

        except Exception as e:
            print(f"[EXEC ERROR] {e}")

    else:
        print("⏸️ 未交易")

    time.sleep(2)
