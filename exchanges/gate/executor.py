from execution.gate_executor import GateExecutor


class Exchange:

    def __init__(self):
        self.executor = GateExecutor()

    def get_market_data(self):
        return self.executor.get_market_data()

    def execute_order(self, signal):
        return self.executor.execute_trade(
            signal["symbol"],
            signal["action"],
            signal["qty"],
            signal["price"]
        )
