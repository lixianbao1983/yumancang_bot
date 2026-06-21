class StrategyEngine:

    def __init__(self):
        self.min_score = 60

    def evaluate(self, signal):

        score = 0

        symbol = signal.get("symbol", "")
        action = signal.get("action", "")

        if "BTC" in symbol or "ETH" in symbol:
            score += 40

        if action == "BUY":
            score += 30
        else:
            score += 20

        return {
            "approved": score >= self.min_score,
            "score": score,
            "symbol": symbol,
            "action": action
        }
