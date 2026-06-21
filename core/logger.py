import time
import os

os.makedirs("logs", exist_ok=True)

def log(msg):
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{t}] {msg}"

    print(line)

    with open("logs/trading.log", "a") as f:
        f.write(line + "\n")
