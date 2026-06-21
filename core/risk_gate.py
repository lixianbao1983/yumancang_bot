class RiskGate:

    def __init__(self):
        self.max_positions = 3
        self.max_loss = -0.05  # 5%（先模拟）

    def check(self, signal, positions):

        # 🧠 1. 仓位数量限制
        if len(positions) >= self.max_positions:
            return False, "MAX POSITION LIMIT"

        # 🧠 2. 基础信号合法性
        if "symbol" not in signal:
            return False, "INVALID SIGNAL"

        return True, "OK"
