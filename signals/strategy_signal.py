class StrategySignal:
    """
    简单实盘策略（测试版）
    """

    def on_tick(self, market_data):

        price = market_data["prices"]["BTC_USDT"]

        # 简单逻辑：随机/趋势占位（你后面会升级AI）
        if price % 2 == 0:
            return {
                "symbol": "BTC_USDT",
                "action": "BUY",
                "qty": 0.001,
                "price": price
            }

        return {
            "symbol": "BTC_USDT",
            "action": "SELL",
            "qty": 0.001,
            "price": price
        }
