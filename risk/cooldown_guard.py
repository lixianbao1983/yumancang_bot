from datetime import datetime, timedelta
from state_manager import StateManager

state = StateManager()

COOLDOWN_SECONDS = 300


def cooldown_active():

    last_trade_time = state.get("last_trade_time")

    if not last_trade_time:
        return False

    last_trade = datetime.fromisoformat(last_trade_time)
    now = datetime.utcnow()

    return (now - last_trade) < timedelta(seconds=COOLDOWN_SECONDS)
