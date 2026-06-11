import json
import os
import threading

STATE_FILE = "state.json"
_lock = threading.Lock()

DEFAULT_STATE = {
    "position": None,
    "entry_price": 0.0,
    "equity": 10000.0,
    "daily_trade_count": 0,
    "running": True
}


def load_state():
    if not os.path.exists(STATE_FILE):
        save_state(DEFAULT_STATE)
        return DEFAULT_STATE

    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        save_state(DEFAULT_STATE)
        return DEFAULT_STATE


def save_state(state):
    with _lock:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
