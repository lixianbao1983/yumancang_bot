import time
import hmac
import hashlib
import requests

class GateAccount:
    def __init__(self):
        self.api_key = "YOUR_API_KEY"
        self.secret = "YOUR_SECRET"
        self.base_url = "https://api.gateio.ws"

    def _sign(self, method, url, body=""):
        t = str(int(time.time()))
        payload = f"{method}\n{url}\n{body}\n{t}"
        sign = hmac.new(
            self.secret.encode(),
            payload.encode(),
            hashlib.sha512
        ).hexdigest()
        return t, sign

    def get_balance(self):
        url = "/api/v4/spot/accounts"

        t, sign = self._sign("GET", url, "")

        headers = {
            "KEY": self.api_key,
            "Timestamp": t,
            "SIGN": sign
        }

        r = requests.get(self.base_url + url, headers=headers)

        return r.json()

    def print_account(self):
        data = self.get_balance()

        print("\n📊 ===== 账户信息 =====")
        for item in data:
            currency = item.get("currency")
            available = item.get("available")
            locked = item.get("locked")

            if float(available) > 0 or float(locked) > 0:
                print(f"{currency}: available={available}, locked={locked}")
