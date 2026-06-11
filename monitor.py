import time
import json
import os
from datetime import datetime

TRADE_FILE = "trading_bot/data/trade_history.json"


# =========================
# 读取交易记录
# =========================
def load_trades(limit=20):
    trades = []

    try:
        with open(TRADE_FILE, "r") as f:
            for line in f:
                try:
                    trades.append(json.loads(line.strip()))
                except:
                    continue
    except FileNotFoundError:
        return []

    return trades[-limit:]


# =========================
# 计算简单统计
# =========================
def calculate_stats(trades):
    if not trades:
        return {
            "total_trades": 0,
            "last_equity": 0,
            "last_cash": 0,
            "symbol": None
        }

    last = trades[-1]

    return {
        "total_trades": len(trades),
        "last_equity": last.get("equity", 0),
        "last_cash": last.get("cash", 0),
        "symbol": last.get("symbol", "-")
    }


# =========================
# 清屏
# =========================
def clear():
    os.system("clear")


# =========================
# 主监控循环
# =========================
def run():
    while True:
        trades = load_trades(20)
        stats = calculate_stats(trades)

        clear()

        print("📊 =============================")
        print("      REALTIME TRADE MONITOR")
        print("===============================")

        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📦 Symbol: {stats['symbol']}")
        print(f"💰 Last Equity: {stats['last_equity']:.2f}")
        print(f"💵 Last Cash: {stats['last_cash']:.2f}")
        print(f"📈 Trades Loaded: {stats['total_trades']}")

        print("\n🧾 Recent Trades:")
        print("-------------------------------")

        for t in trades[-10:]:
            print(
                f"{t['time']} | {t['symbol']} | {t['side']} | "
                f"qty={t['qty']} | price={t['price']} | cash={t['cash']}"
            )

        print("\n🔄 Refreshing every 2s... (CTRL+C to exit)")

        time.sleep(2)


if __name__ == "__main__":
    run()
