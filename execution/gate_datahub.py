class GateDataHub:

    def __init__(self, gate_client=None):
        self.client = gate_client
        self.portfolio = self.format_account()

    def format_account(self):
        return {
            "equity": 10000.0,
            "cash": 8000.0,
            "positions": {}
        }

    def get_account(self):
        return self.portfolio
