import requests
import time
import hmac
import hashlib

api_key = "973f286bbe8fcca1ab77820471df7889"
api_secret = "6c728adc2fddbc1a3f628d31403e9836a3307cb64760422822d03ea120cfe542"

def sign_request(method, url, query_string="", body=""):
    t = str(int(time.time()))

    body_hash = hashlib.sha512(body.encode()).hexdigest()

    payload = f"{method}\n{url}\n{query_string}\n{body_hash}\n{t}"

    sign = hmac.new(
        api_secret.encode(),
        payload.encode(),
        hashlib.sha512
    ).hexdigest()

    headers = {
        "KEY": api_key,
        "Timestamp": t,
        "SIGN": sign
    }

    return headers, t


method = "GET"
url = "/api/v4/spot/accounts"

headers, t = sign_request(method, url)

r = requests.get("https://api.gateio.ws" + url, headers=headers)

print("STATUS:", r.status_code)
print("BODY:", r.text)
