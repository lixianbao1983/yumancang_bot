class Strategy:

    def on_tick(self, market):

        prices = market.get("prices", {})

        if not prices:
            return {"action": "HOLD"}

        symbol = list(prices.keys())[0]
        price = prices[symbol]

        # 简单示例策略
        if price > 100:
            return {
                "symbol": symbol,
                "action": "SELL",
                "qty": 0.001,
                "price": price
            }

        return {
            "action": "HOLD"
        }
