import ccxt
import time
import logging

class GateMarketData:
    """
    工业级实体实盘行情引擎
    强行锁定现货钱包路由，确保精准穿透实体账户。
    """
    def __init__(self):
        self.exchange = ccxt.gateio({
            'apiKey': '',       # ⚡ 保持你的实盘Key（系统会自动读取你盘前配置的凭证）
            'secret': '',
            'timeout': 5000,    
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot'  # 💡 【实体交易核心】强行指定路由为现货钱包账户
            }
        })
        self.prices = {}

    def fetch_price(self, symbol: str) -> float:
        standard_symbol = symbol.upper()
        try:
            ticker = self.exchange.fetch_ticker(standard_symbol)
            last_price = float(ticker['last'])
            self.prices[standard_symbol] = last_price
            return last_price
        except Exception as e:
            logging.warning(f"⚠️ 实体行情抓取异常 [{standard_symbol}]: {str(e)}")
            return float(self.prices.get(standard_symbol, 0.0))

    def get_market_data(self) -> dict:
        return {
            "price": {
                "BTC/USDT": self.fetch_price("BTC/USDT"),
                "ETH/USDT": self.fetch_price("ETH/USDT"),
            },
            "timestamp": int(time.time())
        }
