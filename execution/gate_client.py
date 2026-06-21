import os
import time
import json
import hmac
import hashlib
import requests
from urllib.parse import urlencode



class GateClient:


    def __init__(self, key, secret):

        self.key = key
        self.secret = secret

        self.host = "https://api.gateio.ws"



    def _sign(
        self,
        method,
        path,
        query="",
        body=""
    ):

        t = str(int(time.time()))


        hashed_body = hashlib.sha512(
            body.encode()
        ).hexdigest()



        sign_string = "\n".join(
            [
                method.upper(),
                path,
                query,
                hashed_body,
                t
            ]
        )


        sign = hmac.new(
            self.secret.encode(),
            sign_string.encode(),
            hashlib.sha512
        ).hexdigest()


        return t, sign



    def request(
        self,
        method,
        path,
        params=None,
        body=None
    ):


        if params:

            query = urlencode(params)

        else:

            query = ""



        if body:

            body_str = json.dumps(
                body,
                separators=(",",":")
            )

        else:

            body_str = ""



        t, sign = self._sign(
            method,
            path,
            query,
            body_str
        )



        headers = {

            "KEY": self.key,

            "Timestamp": t,

            "SIGN": sign,

            "Content-Type":
            "application/json"

        }



        url = (
            self.host
            +
            path
        )



        print("========== GATE REQUEST ==========")
        print(method, path)
        print("QUERY:", query)
        print("BODY:", body_str)
        print("==================================")



        r = requests.request(

            method,

            url,

            headers=headers,

            params=params,

            data=body_str,

            timeout=10

        )


        try:

            return r.json()


        except:

            return {

                "status":r.status_code,

                "text":r.text

            }




    def place_order(
        self,
        order
    ):


        # dual_plus账户需要明确仓位模式

        order["auto_size"] = (
            "open_long"
            if order["size"] > 0
            else "open_short"
        )


        return self.request(

            "POST",

            "/api/v4/futures/usdt/orders",

            body=order

        )
