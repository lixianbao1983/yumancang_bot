class MultiCoinStrategy:
    def __init__(self, fast_period: int = 3, slow_period: int = 5):
        self.fast_period = fast_period
        self.slow_period = slow_period
        # 使用字典为每个币种单独开辟一个历史价格内存队列
        self.history_prices = {}
        
    def on_tick(self, tick, tracker) -> dict:
        """
        对输入的特定币种进行独立的市场均线分析与多空判断
        """
        symbol = tick.symbol
        if symbol not in self.history_prices:
            self.history_prices[symbol] = []
            
        self.history_prices[symbol].append(tick.price)
        
        # 保持对应币种的队列长度
        if len(self.history_prices[symbol]) > self.slow_period * 2:
            self.history_prices[symbol].pop(0)
            
        # 数据不够时，该币种保持观望
        if len(self.history_prices[symbol]) < self.slow_period:
            return {"symbol": symbol, "side": "HOLD", "qty": 0.0, "price": tick.price}
            
        # 计算当前币种的快慢均线
        prices = self.history_prices[symbol]
        fast_ma = sum(prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(prices[-self.slow_period:]) / self.slow_period
        
        print(f"📊 [ANALYSIS] 市场分析 -> {symbol} | 当前价: {tick.price} | 快线: {fast_ma:.2f} | 慢线: {slow_ma:.2f}")
        
        # 获取该币种的当前真实持仓量
        coin_quantity = tracker.get_quantity(symbol)
        
        # 均线多空金叉死叉分析
        if fast_ma > slow_ma and coin_quantity == 0:
            # 金叉多头爆发 -> 触发买入信号
            qty_to_buy = 0.05 if "BTC" in symbol else (0.5 if "ETH" in symbol else 5.0)
            return {"symbol": symbol, "side": "BUY", "qty": qty_to_buy, "price": tick.price}
        elif fast_ma < slow_ma and coin_quantity > 0:
            # 死叉多头衰竭 -> 触发平仓信号
            return {"symbol": symbol, "side": "SELL", "qty": coin_quantity, "price": tick.price}
            
        return {"symbol": symbol, "side": "HOLD", "qty": 0.0, "price": tick.price}
