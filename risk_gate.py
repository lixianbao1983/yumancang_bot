class RiskGate:
    def check(self, state, signal):
        if not state.get("running"):
            return False, "STOPPED"

        if state.get("daily_trade_count", 0) > 10:
            return False, "LIMIT"

        return True, "OK"
