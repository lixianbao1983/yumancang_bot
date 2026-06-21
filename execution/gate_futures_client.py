import time
import hashlib
import hmac
import requests
import json


class GateFuturesClient:


    def __init__(
        self,
        api_key: str,
        api_secret: str,
        host: str = "https://gateio.ws"
    ):

        self.api_key = api_key
        self.api_secret = api_secret
        self.host = host
        self.prefix = "/api/v4"



    def _sign(
        self,
        method: str,
        path: str,
        query_string: str,
        body_str: str,
        timestamp: str
    ) -> str:

        body_hash = hashlib.sha512(
            body_str.encode("utf-8")
        ).hexdigest()


        sign_text = (
            f"{method}\n"
            f"{path}\n"
            f"{query_string}\n"
            f"{body_hash}\n"
            f"{timestamp}"
        )


        sign_bytes = hmac.new(
            self.api_secret.encode("utf-8"),
            sign_text.encode("utf-8"),
            hashlib.sha512
        ).digest()


        return sign_bytes.hex()



    def place_order(
        self,
        order_payload: dict
    ) -> dict:


        path = f"{self.prefix}/futures/usdt/orders"

        url = f"{self.host}{path}"

        method = "POST"

        query_string = ""


        body_str = json.dumps(
            order_payload,
            separators=(",", ":")
        )


        timestamp = str(int(time.time()))



        headers = {

            "Accept": "application/json",

            "Content-Type": "application/json",

            "KEY": self.api_key,

            "Timestamp": timestamp,

            "SIGN": self._sign(
                method,
                path,
                query_string,
                body_str,
                timestamp
            )

        }



        print("\n" + "=" * 60)

        print("📡 [Gate v2 Client] 发送请求:")

        print(f"🔗 URL: {url}")

        print(f"⏱️ TIMESTAMP: {timestamp}")

        print(f"📦 PAYLOAD: {body_str}")

        print("=" * 60)



        try:

            resp = requests.post(
                url,
                headers=headers,
                data=body_str,
                timeout=10
            )


            print(f"📥 STATUS CODE: {resp.status_code}")

            print(f"📄 RESPONSE: {resp.text}")



            if resp.status_code in [200, 201]:

                return resp.json()



            else:

                return {

                    "error": True,

                    "status": resp.status_code,

                    "message": resp.text

                }



        except requests.exceptions.RequestException as e:


            return {

                "error": True,

                "message": str(e)

            }
