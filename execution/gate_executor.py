class GateExecutor:

    def __init__(self, client=None):
        self.client = client

    def execute(self, signal):

        print("EXECUTE:", signal)

        return {
            "price": 100
        }
