import time
from core.position_manager import PositionManager
from core.memory import Memory
from core.risk_gate import RiskGate
from execution.market_watcher import MarketWatcher
from strategy.signal_engine import SignalEngine

class AutonomousEngine:

    def __init__(self):
        self.pm = PositionManager()
        self.memory = Memory()
        self.risk = RiskGate()
        self.watcher = MarketWatcher()
        self.signal_engine = SignalEngine()
        self.interval = 3

    def run(self):

        print("🚀 ENGINE STARTED")

        while True:

            # 🧠 1. 获取价格
            price = self.watcher.scan("BTC_USDT")

            if price is None:
                time.sleep(self.interval)
                continue

            symbol = "BTC_USDT"

            # 🧠 2. 更新持仓浮动盈亏（关键！）
            self.pm.update_price(symbol, price)

            # 🧠 3. 生成信号
            signal = self.signal_engine.generate(symbol, price)

            if not signal:
                time.sleep(self.interval)
                continue

            # 🧠 4. 冷却控制
            if not self.memory.can_trade():
                print("⏳ COOLDOWN ACTIVE")
                time.sleep(self.interval)
                continue

            # 🧠 5. 风控
            ok, reason = self.risk.check(signal, self.pm.get_positions())

            if not ok:
                print(f"🛑 REJECT: {reason}")
                time.sleep(self.interval)
                continue

            # 🧠 6. 仓位检查
            if self.pm.has_position(symbol):
                print(f"⛔ ALREADY HOLD: {symbol}")
                time.sleep(self.interval)
                continue

            # 🧠 7. 执行交易
            self.pm.open_position(signal, price)
            self.memory.update_trade()

            time.sleep(self.interval)
