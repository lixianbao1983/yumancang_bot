import time
import hmac
import hashlib
import requests


class GateClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.gateio.ws"

    # ======================
    # 签名
    # ======================
    def _sign(self, method, url, query_string="", body=""):
        t = str(int(time.time()))

        body_hash = hashlib.sha512(body.encode()).hexdigest()
        payload = f"{method}\n{url}\n{query_string}\n{body_hash}\n{t}"

        sign = hmac.new(
            self.api_secret.encode(),
            payload.encode(),
            hashlib.sha512
        ).hexdigest()

        return t, sign

    def _headers(self, t, sign):
        return {
            "KEY": self.api_key,
            "Timestamp": t,
            "SIGN": sign,
            "Content-Type": "application/json"
        }

    # ======================
    # 行情
    # ======================
    def get_ticker(self, symbol):
        url = f"/api/v4/spot/tickers?currency_pair={symbol}"
        r = requests.get(self.base_url + url)
        return r.json()

    # ======================
    # 账户
    # ======================
    def get_balances(self):
        url = "/api/v4/spot/accounts"

        t, sign = self._sign("GET", url)

        r = requests.get(
            self.base_url + url,
            headers=self._headers(t, sign)
        )

        return r.json()

    # ======================
    # 下单
    # ======================
    def place_order(self, symbol, side, amount, price=None):
        import json

        url = "/api/v4/spot/orders"

        body = {
            "currency_pair": symbol,
            "type": "market",
            "side": side.lower(),
            "amount": str(amount)
        }

        body_str = json.dumps(body)

        t, sign = self._sign("POST", url, "", body_str)

        r = requests.post(
            self.base_url + url,
            headers=self._headers(t, sign),
            data=body_str
        )

        return r.json()
