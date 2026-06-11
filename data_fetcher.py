import math
import time
import random
from engine_base import MarketTick


class LiveMarketStream:
    def __init__(self):
        self.base = {
            "BTC_USDT": 68000,
            "ETH_USDT": 3500
        }
        self.cnt = {"BTC_USDT": 0, "ETH_USDT": 0}

    def fetch_live_ticks(self):
        ticks = {}

        for symbol in self.base:
            self.cnt[symbol] += 1
            c = self.cnt[symbol]

            noise = random.uniform(-5, 5)
            wave = math.sin(c * 0.1) * 50

            price = self.base[symbol] + wave + noise

            ticks[symbol] = MarketTick(symbol, round(price, 2))

        return ticks
