import importlib
import os


class StrategyLoader:

    def __init__(self, strategy_path="strategies"):
        self.strategy_path = strategy_path
        self.strategies = []

    def load(self):
        self.strategies = []

        for folder in os.listdir(self.strategy_path):
            full_path = os.path.join(self.strategy_path, folder)

            if not os.path.isdir(full_path):
                continue

            try:
                module_path = f"{self.strategy_path}.{folder}.strategy"
                module = importlib.import_module(module_path)

                strategy_class = getattr(module, "Strategy")
                self.strategies.append(strategy_class())

                print(f"[LOADED STRATEGY] {folder}")

            except Exception as e:
                print(f"[SKIP] {folder} -> {e}")

        return self.strategies
