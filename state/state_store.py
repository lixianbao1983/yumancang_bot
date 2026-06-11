import json
import os

STATE_FILE = "state/trade_state.json"

DEFAULT_STATE = {
    "position": None,
    "entry_price": 0,
    "last_trade_time": None,
    "daily_trade_count": 0,
    "equity": 10000
}


def load_state():

    if not os.path.exists(STATE_FILE):
        save_state(DEFAULT_STATE)
        return DEFAULT_STATE

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)
