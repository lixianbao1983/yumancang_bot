class FourBrainAgent:
    def __init__(self, memory_len=5):
        self.memory = []
        self.memory_len = memory_len

    def _safe_market_data(self, market_data):
        if not isinstance(market_data, dict):
            return {"prices": {}}
        return {"prices": market_data.get("prices", {})}

    def _left_market_brain(self, market_data):
        prices = market_data["prices"]
        btc = prices.get("BTC/USDT", 0)
        if btc > 100:
            return "BUY", 0.6
        return "HOLD", 0.3

    def _right_reasoning_brain(self, market_data):
        return "HOLD", 0.5

    def _cerebellum_brain(self, market_data):
        return 0.0

    def think_and_vote(self, market_data):
        data = self._safe_market_data(market_data)

        l, lc = self._left_market_brain(data)
        r, rc = self._right_reasoning_brain(data)
        c = self._cerebellum_brain(data)

        score = 0
        if l == "BUY": score += lc
        if l == "SELL": score -= lc
        if r == "BUY": score += rc
        if r == "SELL": score -= rc

        score += c

        if score > 0.5:
            signal = "BUY"
        elif score < -0.5:
            signal = "SELL"
        else:
            signal = "HOLD"

        return {
            "signal": signal,
            "score": score
        }


_global_agent = FourBrainAgent()

def get_signal(market_data: dict):
    return _global_agent.think_and_vote(market_data)
