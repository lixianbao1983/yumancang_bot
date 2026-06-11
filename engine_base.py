import time

class MarketTick:
    def __init__(self, symbol, price, timestamp=None):
        self.symbol = symbol
        self.price = price
        self.timestamp = timestamp or time.time()

    def __repr__(self):
        return f"MarketTick(symbol={self.symbol}, price={self.price}, time={self.timestamp})"
