import requests

class MarketWatcher:

    def get_price(self, symbol):

        try:
            url = "https://api.gateio.ws/api/v4/futures/usdt/tickers"
            r = requests.get(url, timeout=5)
            data = r.json()

            for item in data:
                if item["contract"] == symbol:
                    return float(item["last"])
        except:
            return None

    def scan(self, symbol="BTC_USDT"):
        return self.get_price(symbol)
