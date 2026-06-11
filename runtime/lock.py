import os
import sys

LOCK_FILE = "/tmp/trading_bot.lock"

def check_single_instance():
    if os.path.exists(LOCK_FILE):
        print("[SYSTEM BLOCK] Trading bot already running!")
        sys.exit(1)

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
