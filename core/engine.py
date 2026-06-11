import importlib
import time
import yaml


class Engine:

    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.exchange = self._load_exchange()
        self.strategies = self._load_strategies()

    # ===== 动态加载交易所 =====
    def _load_exchange(self):
        name = self.config["exchange"]
        module = importlib.import_module(f"exchanges.{name}.executor")
        return module.Exchange()

    # ===== 动态加载策略 =====
    def _load_strategies(self):
        strategies = []
        for s in self.config["strategies"]:
            module = importlib.import_module(f"strategies.{s}.strategy")
            strategies.append(module.Strategy())
        return strategies

    # ===== 主循环 =====
    def run(self):
        print("🚀 Engine started")

        while True:

            market = self.exchange.get_market_data()

            for strat in self.strategies:
                signal = strat.on_tick(market)

                if signal["action"] == "HOLD":
                    continue

                print(f"⚡ SIGNAL: {signal}")

                self.exchange.execute_order(signal)

            time.sleep(2)
