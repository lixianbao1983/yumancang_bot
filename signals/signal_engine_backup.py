def think_and_vote(self, market_data: dict) -> dict:
    data = self._safe_market_data(market_data)

    left_side, left_conf = self._left_market_brain(data)
    right_side, right_conf = self._right_reasoning_brain(data)
    cerebellum = self._cerebellum_brain(data)

    # ===== 投票逻辑 =====
    score = 0

    if left_side == "BUY":
        score += left_conf
    elif left_side == "SELL":
        score -= left_conf

    if right_side == "BUY":
        score += right_conf
    elif right_side == "SELL":
        score -= right_conf

    score += cerebellum

    # ===== 输出决策 =====
    if score > 0.5:
        signal = "BUY"
    elif score < -0.5:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "signal": signal,
        "score": score,
        "left": left_side,
        "right": right_side,
        "cerebellum": cerebellum
    }
